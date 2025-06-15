"""
engine/gui/other/slots/unit_slot.py

Specialized slot for craft personnel assignments in the XCOM GUI.

Classes:
    TUnitSlot: Slot for unit assignments to craft crew positions.

Last standardized: 2025-06-15
"""

from typing import Optional, Dict
from gui.other.slots.inventory_slot import TInventorySlot
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QDrag, QCursor, QMimeData
from PySide6.QtWidgets import QToolTip
from unit.unit import TUnit


class TUnitSlot(TInventorySlot):
    """
    Slot for unit assignments to craft crew positions.
    Always contains a single TUnit or None (empty).

    Attributes:
        crewChanged (Signal): Emitted when craft capabilities change due to crew changes.
    """

    # Signal emitted when craft capabilities change due to crew changes
    crewChanged = Signal(object)  # Emits the unit object

    def __init__(
        self,
        parent=None,
        position_type=None,  # e.g., "pilot", "navigator", "soldier"
        position_name="",
        size=64,
        border_width=2,
        accept_types=None,  # List of unit types that can be assigned to this position
        bg_color="#1E2836",
        border_color="#30465d",
        hover_color="#3399ff",
        locked=False
    ):
        """
        Initialize craft unit slot with custom properties.

        Args:
            parent: Parent widget.
            position_type: Type of crew position (e.g., pilot).
            position_name: Name of the position.
            size: Size of the slot in pixels.
            border_width: Border width in pixels.
            accept_types: List of accepted unit types.
            bg_color: Background color.
            border_color: Border color.
            hover_color: Hover color.
            locked: If True, slot is locked.
        """
        super().__init__(
            parent=parent,
            slot_type=position_type,
            slot_name=position_name,
            size=size,
            border_width=border_width,
            accept_types=accept_types,
            bg_color=bg_color,
            border_color=border_color,
            hover_color=hover_color,
            locked=locked
        )

        # Unit-specific properties
        self.unit: Optional[TUnit] = None
        self.requirements: Dict[str, int] = {}  # Position requirements (e.g., piloting skill)
        self.position_type = position_type
        self.position_name = position_name

        # Set mime type for drag and drop
        self.setAcceptDrops(True)
        self.mime_type = "application/x-unit"

    def set_unit(self, unit: Optional[TUnit]):
        """
        Assign a unit to this craft position or remove unit if None.

        Args:
            unit: The unit to assign or None to clear the position
        """
        prev_unit = self.unit
        self.unit = unit

        # Update the display with the new unit
        self.update_display()

        # Emit signal that crew has changed
        if prev_unit != unit:
            self.crewChanged.emit(unit)

    def get_unit(self) -> Optional[TUnit]:
        """
        Get the currently assigned unit.

        Returns:
            The unit assigned to this position or None if empty
        """
        return self.unit

    def update_display(self):
        """Update the visual representation of the slot based on current unit."""
        # Clear previous display
        self.clear_display()

        if not self.unit:
            self.set_empty_appearance()
            return

        # Set unit sprite if available
        if hasattr(self.unit, 'get_sprite') and callable(getattr(self.unit, 'get_sprite')):
            sprite = self.unit.get_sprite()
            if sprite:
                self.set_image(sprite)

        # Update tooltip with unit info
        self.update_tooltip()

    def update_tooltip(self):
        """Update tooltip with detailed unit information."""
        if not self.unit:
            self.setToolTip(f"Empty {self.position_name} position")
            return

        # Build tooltip with unit details
        tooltip = f"<b>{self.unit.name}</b><br>"
        tooltip += f"Role: {self.position_name}<br>"

        # Add stats if available
        if hasattr(self.unit, 'rank'):
            tooltip += f"Rank: {self.unit.rank}<br>"
        if hasattr(self.unit, 'skills') and isinstance(self.unit.skills, dict):
            relevant_skills = []
            if self.position_type == "pilot" and "piloting" in self.unit.skills:
                relevant_skills.append(f"Piloting: {self.unit.skills['piloting']}")
            elif self.position_type == "navigator" and "navigation" in self.unit.skills:
                relevant_skills.append(f"Navigation: {self.unit.skills['navigation']}")

            if relevant_skills:
                tooltip += "<br>".join(relevant_skills)

        self.setToolTip(tooltip)

    def set_empty_appearance(self):
        """Set appearance for an empty position slot."""
        self.clear_display()
        self.setText(self.position_name)

    def can_accept_unit(self, unit) -> bool:
        """
        Check if this position can accept the specified unit.

        Args:
            unit: Unit to validate for this position

        Returns:
            True if the unit can be assigned to this position
        """
        if not unit:
            return False

        # Check unit type compatibility
        if self.accept_types and unit.unit_type not in self.accept_types:
            return False

        # Check position-specific requirements
        if self.position_type == "pilot" and hasattr(unit, 'skills'):
            if unit.skills.get('piloting', 0) < self.requirements.get('piloting', 0):
                return False

        elif self.position_type == "navigator" and hasattr(unit, 'skills'):
            if unit.skills.get('navigation', 0) < self.requirements.get('navigation', 0):
                return False

        return True

    def mousePressEvent(self, event):
        """Handle mouse press events for drag and drop."""
        if event.button() == Qt.LeftButton and self.unit and not self.locked:
            # Start drag operation
            drag = QDrag(self)
            mime_data = self.create_mime_data()
            drag.setMimeData(mime_data)

            # Create pixmap for drag visual
            pixmap = self.create_drag_pixmap()
            if pixmap:
                drag.setPixmap(pixmap)

            # Start drag operation
            if drag.exec_() == Qt.MoveAction:
                # Unit was moved successfully
                self.set_unit(None)

        elif event.button() == Qt.RightButton and self.unit:
            # Implement right-click action (e.g., show unit details or quick-return to barracks)
            self.handle_right_click()

        super().mousePressEvent(event)

    def create_mime_data(self):
        """Create mime data for drag and drop operations."""
        mime_data = super().create_mime_data() if hasattr(super(), 'create_mime_data') else QMimeData()

        if self.unit:
            # Serialize unit ID or reference for transfer
            unit_data = {"unit_id": self.unit.id if hasattr(self.unit, 'id') else str(id(self.unit))}
            mime_data.setData(self.mime_type, str(unit_data).encode())

        return mime_data

    def create_drag_pixmap(self):
        """Create a pixmap for drag operation visualization."""
        if not self.unit or not hasattr(self.unit, 'get_sprite') or not callable(getattr(self.unit, 'get_sprite')):
            return None

        sprite = self.unit.get_sprite()
        if not sprite:
            return None

        # Create pixmap from unit sprite
        return sprite.scaled(QSize(self.size, self.size), Qt.KeepAspectRatio)

    def handle_right_click(self):
        """Handle right-click action on assigned unit."""
        # Example: Show detailed unit information or context menu
        if self.unit:
            # Show more detailed tooltip
            unit_details = self.get_detailed_unit_info()
            QToolTip.showText(QCursor.pos(), unit_details)

    def get_detailed_unit_info(self) -> str:
        """Get detailed information about the assigned unit."""
        if not self.unit:
            return "No unit assigned"

        # Build detailed unit information for tooltip or context menu
        details = f"<b>{self.unit.name}</b><br>"
        details += f"Position: {self.position_name}<br><br>"

        # Add stats if available
        if hasattr(self.unit, 'rank'):
            details += f"<b>Rank:</b> {self.unit.rank}<br>"

        # Add skills section if available
        if hasattr(self.unit, 'skills') and isinstance(self.unit.skills, dict):
            details += "<b>Skills:</b><br>"
            for skill_name, skill_value in self.unit.skills.items():
                details += f"• {skill_name.capitalize()}: {skill_value}<br>"

        # Add other relevant info
        if hasattr(self.unit, 'experience'):
            details += f"<b>Experience:</b> {self.unit.experience}<br>"
        if hasattr(self.unit, 'missions'):
            details += f"<b>Missions:</b> {self.unit.missions}<br>"

        return details

    def dragEnterEvent(self, event):
        """Handle drag enter events for validation."""
        if event.mimeData().hasFormat(self.mime_type):
            # Check if we can accept this unit
            # In a real implementation, you would decode the mime data and check the unit
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Handle drop events to assign units."""
        if event.mimeData().hasFormat(self.mime_type):
            # In a real implementation, you would:
            # 1. Extract the unit ID from the mime data
            # 2. Retrieve the actual unit from game state
            # 3. Verify compatibility
            # 4. Assign the unit

            # Example placeholder:
            event.acceptProposedAction()
            # self.set_unit(unit_from_mime_data)  # Would be implemented in real code
        else:
            event.ignore()
