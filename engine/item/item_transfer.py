"""
TItemTransferManager: Manages the transfer of items between inventory slots.
Purpose: Handles drag-and-drop, compatibility checks, swap logic, and undo/redo history for inventory systems.
Last update: 2025-06-10
"""

from typing import Dict, Optional, Any, Callable, Tuple
from PySide6.QtCore import QObject, Signal, Qt, QMimeData, QByteArray
from PySide6.QtGui import QDrag
from PySide6.QtWidgets import QWidget

class TItemTransferManager(QObject):
    """
    Manages the transfer of items between inventory slots.

    Handles drag-and-drop, compatibility checks, swap logic, and undo/redo history for inventory systems.

    Attributes:
        item_transfer_started: Signal emitted when a transfer starts.
        item_transfer_completed: Signal emitted when a transfer completes.
        item_transfer_cancelled: Signal emitted when a transfer is cancelled.
        inventory_updated: Signal emitted when inventory changes.
        MIME_TYPE: MIME type for drag-and-drop.
        _current_drag_item: The item currently being dragged.
        _source_widget: The widget where the drag started.
        _source_id: The ID of the source slot.
        _validate_slot_compatibility: Function to check slot compatibility.
        _history: List of inventory actions for undo/redo.
        _history_index: Current index in the history.
        _history_max: Maximum history size.
        _swap_buffer: Temporary buffer for item swaps.
    """

    # Define signals for item transfer events
    item_transfer_started = Signal(str, object)  # source_id, item
    item_transfer_completed = Signal(str, str, object)  # source_id, target_id, item
    item_transfer_cancelled = Signal(str, object)  # source_id, item
    inventory_updated = Signal()  # Generic update signal
    
    # MIME type for internal drag and drop operations
    MIME_TYPE = "application/x-xcom-item"
    
    def __init__(self, validate_slot_compatibility: Optional[Callable] = None):
        """
        Initialize the item transfer manager.

        Args:
            validate_slot_compatibility: Optional function to check if an item can be placed in a slot.
                Should take (item, slot) and return True if compatible.
        """
        super().__init__()
        self._current_drag_item = None
        self._source_widget = None
        self._source_id = None
        self._validate_slot_compatibility = validate_slot_compatibility or self._default_validate_compatibility
        
        # Track inventory changes for undo/redo functionality
        self._history = []
        self._history_index = -1
        self._history_max = 20
        
        # Container for temp holding when swapping items
        self._swap_buffer = None
        
    def _default_validate_compatibility(self, item: Any, slot: Any) -> bool:
        """
        Default validation function if none is provided.
        Checks item type against slot type.

        Args:
            item: Item being transferred.
            slot: Target slot.
        Returns:
            True if compatible, False otherwise.
        """
        # Default implementation - can be overridden with custom logic
        if not hasattr(slot, 'compatible_types'):
            return True
            
        if not hasattr(item, 'item_type'):
            return True
            
        return item.item_type in slot.compatible_types
    
    def start_drag(self, source_widget: QWidget, item: Any, source_id: str) -> bool:
        """
        Begin dragging an item from a source widget.

        Args:
            source_widget: Widget that initiated the drag.
            item: The item being dragged.
            source_id: Unique identifier for the source.
        Returns:
            True if drag initiated successfully, False otherwise.
        """
        if not item:
            return False
            
        self._current_drag_item = item
        self._source_widget = source_widget
        self._source_id = source_id
        
        # Create mime data for the drag operation
        mime_data = QMimeData()
        mime_data.setData(self.MIME_TYPE, QByteArray(source_id.encode()))
        
        # Create drag object
        drag = QDrag(source_widget)
        drag.setMimeData(mime_data)
        
        # Set drag icon with item's pixmap if available
        if hasattr(item, 'get_pixmap'):
            pixmap = item.get_pixmap(48)
            drag.setPixmap(pixmap)
            drag.setHotSpot(pixmap.rect().center())
        
        # Emit signal that drag has started
        self.item_transfer_started.emit(source_id, item)
        
        # Execute drag and handle result
        result = drag.exec_(Qt.MoveAction if hasattr(Qt, 'MoveAction') else 2)

        if result == (Qt.IgnoreAction if hasattr(Qt, 'IgnoreAction') else 0):
            # Drag was cancelled
            self.item_transfer_cancelled.emit(source_id, item)
            self._reset_drag_state()
            return False
            
        return True
    
    def can_accept_drop(self, target_widget: QWidget, target_id: str, mime_data: QMimeData) -> bool:
        """
        Check if the target can accept the current drag item.

        Args:
            target_widget: Widget receiving the drop.
            target_id: Unique identifier for the target.
            mime_data: Drag operation's mime data.
        Returns:
            True if drop can be accepted, False otherwise.
        """
        # Verify MIME type
        if not mime_data.hasFormat(self.MIME_TYPE):
            return False
            
        # Don't allow dropping onto self unless explicitly allowed
        source_id = mime_data.data(self.MIME_TYPE).data().decode()
        if source_id == target_id and not getattr(target_widget, 'allow_self_drop', False):
            return False
            
        # Check if we have a current drag item
        if not self._current_drag_item:
            return False
            
        # Validate compatibility
        return self._validate_slot_compatibility(self._current_drag_item, target_widget)
    
    def accept_drop(self, target_widget: QWidget, target_id: str, mime_data: QMimeData) -> Tuple[bool, Any, Any]:
        """
        Accept a drop on a target widget.

        Args:
            target_widget: Widget receiving the drop.
            target_id: Unique identifier for the target.
            mime_data: Drag operation's mime data.
        Returns:
            Tuple of (success, source_item, target_item).
        """
        if not self.can_accept_drop(target_widget, target_id, mime_data):
            return False, None, None
            
        # Get source information
        source_id = mime_data.data(self.MIME_TYPE).data().decode()
        source_item = self._current_drag_item
        
        # Get the target's current item if any
        target_item = getattr(target_widget, 'item', None)
        
        # Handle item swap or move
        self._handle_item_swap(source_id=source_id,
                              target_id=target_id,
                              source_widget=self._source_widget,
                              target_widget=target_widget,
                              source_item=source_item,
                              target_item=target_item)
        
        # Emit transfer completed signal
        self.item_transfer_completed.emit(source_id, target_id, source_item)
        
        # Reset the drag state
        self._reset_drag_state()
        
        # Emit general inventory update
        self.inventory_updated.emit()
        
        return True, source_item, target_item
    
    def _handle_item_swap(self, source_id: str, target_id: str,
                         source_widget: QWidget, target_widget: QWidget,
                         source_item: Any, target_item: Any) -> None:
        """
        Handle swapping items between slots or moving to an empty slot.

        Args:
            source_id: ID of the source slot.
            target_id: ID of the target slot.
            source_widget: Widget containing the source item.
            target_widget: Widget receiving the item.
            source_item: Item being dragged.
            target_item: Item in the target slot (can be None).
        """
        # Handle simple item movement (no target item)
        if not target_item:
            if hasattr(source_widget, 'remove_item'):
                source_widget.remove_item()
            
            if hasattr(target_widget, 'add_item'):
                target_widget.add_item(source_item)
            return
        
        # Handle swap (both slots have items)
        self._swap_buffer = target_item
        
        # Remove items from both slots
        if hasattr(source_widget, 'remove_item'):
            source_widget.remove_item()
        
        if hasattr(target_widget, 'remove_item'):
            target_widget.remove_item()
        
        # Add items to their new slots
        if hasattr(target_widget, 'add_item'):
            target_widget.add_item(source_item)
        
        if hasattr(source_widget, 'add_item'):
            source_widget.add_item(self._swap_buffer)
        
        self._swap_buffer = None
    
    def _reset_drag_state(self) -> None:
        """
        Reset internal drag state variables.
        """
        self._current_drag_item = None
        self._source_widget = None
        self._source_id = None
    
    def get_current_drag_item(self) -> Any:
        """
        Get the item currently being dragged.

        Returns:
            The current drag item, or None if no drag is active.
        """
        return self._current_drag_item
    
    def get_source_widget(self) -> Optional[QWidget]:
        """
        Get the source widget of the current drag operation.

        Returns:
            The source widget, or None if no drag is active.
        """
        return self._source_widget
    
    def get_source_id(self) -> Optional[str]:
        """
        Get the source ID of the current drag operation.

        Returns:
            The source ID, or None if no drag is active.
        """
        return self._source_id
    
    def record_inventory_action(self, action: Dict[str, Any]) -> None:
        """
        Record an inventory action for potential undo/redo.

        Args:
            action: Dictionary describing the action with at least:
                - 'type': Type of action ('move', 'equip', 'unequip', etc)
                - 'source': Source location
                - 'target': Target location
                - 'item_id': ID of affected item
                - Other action-specific fields
        """
        # Truncate any redo history if we're not at the end
        if self._history_index < len(self._history) - 1:
            self._history = self._history[:self._history_index + 1]
        
        # Add new action
        self._history.append(action)
        self._history_index = len(self._history) - 1
        
        # Limit history size
        if len(self._history) > self._history_max:
            self._history = self._history[-self._history_max:]
            self._history_index = len(self._history) - 1
    
    def undo(self) -> bool:
        """
        Undo the last inventory action if possible.

        Returns:
            True if an action was undone, False otherwise.
        """
        if self._history_index < 0:
            return False
            
        # Get the action to undo
        action = self._history[self._history_index]
        
        # Perform the reverse action
        # Implementation depends on action types
        
        # Move history pointer
        self._history_index -= 1
        
        # Signal that inventory has changed
        self.inventory_updated.emit()
        
        return True
    
    def redo(self) -> bool:
        """
        Redo the previously undone inventory action if possible.

        Returns:
            True if an action was redone, False otherwise.
        """
        if self._history_index >= len(self._history) - 1:
            return False
            
        # Move history pointer
        self._history_index += 1
        
        # Get the action to redo
        action = self._history[self._history_index]
        
        # Perform the action
        # Implementation depends on action types
        
        # Signal that inventory has changed
        self.inventory_updated.emit()
        
        return True
    
    def get_item_compatibility_report(self, item: Any, slot: Any) -> Dict[str, Any]:
        """
        Get detailed compatibility information for an item and slot.

        Args:
            item: The item to check.
            slot: The slot to check against.
        Returns:
            Dictionary with compatibility details:
                - compatible: Boolean indicating if item can be placed in slot
                - reason: String explaining incompatibility if applicable
                - warnings: List of warning messages if applicable (e.g., not optimal)
        """
        result = {
            'compatible': False,
            'reason': '',
            'warnings': []
        }
        
        # Basic compatibility check
        basic_compatible = self._validate_slot_compatibility(item, slot)
        result['compatible'] = basic_compatible
        
        if not basic_compatible:
            result['reason'] = "Item type incompatible with slot type"
            return result
        
        # Advanced checks could be added here based on item and slot properties
        # For example, weight limits, special requirements, etc.
        
        # Check if this is the optimal slot (even if compatible)
        # Example: Pistol in primary weapon slot might work but not be optimal
        if hasattr(slot, 'preferred_types') and hasattr(item, 'item_type'):
            if item.item_type not in slot.preferred_types:
                result['warnings'].append("This item is compatible but not optimal for this slot")
        
        return result
