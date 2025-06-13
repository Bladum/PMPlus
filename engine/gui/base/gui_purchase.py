"""
Purchase System GUI Interface
Purpose: Provides user interface for purchasing items, units, and crafts
Last update: 2025-06-12
"""

from typing import Dict, List, Optional, Any
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QListWidget, QListWidgetItem, QComboBox, QSpinBox,
    QTabWidget, QTextEdit, QMessageBox, QGroupBox
)
from PySide6.QtGui import QFont, QIcon

from ..gui.base.gui_core_screen import TGuiCoreScreen
from ..gui.theme_manager import XcomStyle


class TPurchaseGui(TGuiCoreScreen):
    """
    Purchase system interface for buying items, units, and crafts.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Purchasing")
        self.purchase_system = None
        self.current_base = None
        
        self._setup_ui()
        self._refresh_data()
    
    def _setup_ui(self):
        """Setup the user interface."""
        main_layout = QVBoxLayout(self)
        
        # Header with base info and budget
        header = self._create_header()
        main_layout.addWidget(header)
        
        # Main content with tabs
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet(XcomStyle.tab_widget_style())
        
        # Regular purchases tab
        regular_tab = self._create_regular_purchases_tab()
        tab_widget.addTab(regular_tab, "Standard Purchases")
        
        # Black market tab
        black_market_tab = self._create_black_market_tab()
        tab_widget.addTab(black_market_tab, "Black Market")
        
        # Orders status tab
        orders_tab = self._create_orders_tab()
        tab_widget.addTab(orders_tab, "Active Orders")
        
        main_layout.addWidget(tab_widget)
    
    def _create_header(self):
        """Create header with base info and budget."""
        header = QGroupBox("Purchase Information")
        header.setStyleSheet(XcomStyle.group_box_style())
        layout = QHBoxLayout(header)
        
        # Base info
        self.base_label = QLabel("Base: Not Selected")
        self.base_label.setStyleSheet(XcomStyle.label_style())
        layout.addWidget(self.base_label)
        
        layout.addStretch()
        
        # Budget info
        self.budget_label = QLabel("Budget: $0")
        self.budget_label.setStyleSheet(XcomStyle.label_style())
        layout.addWidget(self.budget_label)
        
        return header
    
    def _create_regular_purchases_tab(self):
        """Create tab for regular purchases."""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        # Left side - available purchases
        left_panel = QGroupBox("Available Purchases")
        left_panel.setStyleSheet(XcomStyle.group_box_style())
        left_layout = QVBoxLayout(left_panel)
        
        # Category filter
        category_layout = QHBoxLayout()
        category_layout.addWidget(QLabel("Category:"))
        self.category_combo = QComboBox()
        self.category_combo.addItems(["All", "Items", "Units", "Crafts"])
        self.category_combo.currentTextChanged.connect(self._filter_purchases)
        category_layout.addWidget(self.category_combo)
        category_layout.addStretch()
        left_layout.addLayout(category_layout)
        
        # Purchase list
        self.purchase_list = QListWidget()
        self.purchase_list.setStyleSheet(XcomStyle.list_widget_style())
        self.purchase_list.itemSelectionChanged.connect(self._on_purchase_selected)
        left_layout.addWidget(self.purchase_list)
        
        layout.addWidget(left_panel, 2)
        
        # Right side - purchase details and controls
        right_panel = QGroupBox("Purchase Details")
        right_panel.setStyleSheet(XcomStyle.group_box_style())
        right_layout = QVBoxLayout(right_panel)
        
        # Purchase info
        self.purchase_info = QTextEdit()
        self.purchase_info.setStyleSheet(XcomStyle.text_edit_style())
        self.purchase_info.setMaximumHeight(150)
        self.purchase_info.setReadOnly(True)
        right_layout.addWidget(self.purchase_info)
        
        # Quantity control
        quantity_layout = QHBoxLayout()
        quantity_layout.addWidget(QLabel("Quantity:"))
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)
        self.quantity_spin.setMaximum(100)
        self.quantity_spin.valueChanged.connect(self._update_total_cost)
        quantity_layout.addWidget(self.quantity_spin)
        quantity_layout.addStretch()
        right_layout.addLayout(quantity_layout)
        
        # Total cost
        self.total_cost_label = QLabel("Total Cost: $0")
        self.total_cost_label.setStyleSheet(XcomStyle.label_style())
        right_layout.addWidget(self.total_cost_label)
        
        # Purchase button
        self.purchase_button = QPushButton("Purchase")
        self.purchase_button.setStyleSheet(XcomStyle.button_style())
        self.purchase_button.clicked.connect(self._make_purchase)
        self.purchase_button.setEnabled(False)
        right_layout.addWidget(self.purchase_button)
        
        right_layout.addStretch()
        layout.addWidget(right_panel, 1)
        
        return widget
    
    def _create_black_market_tab(self):
        """Create tab for black market purchases."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        info_label = QLabel("Black Market - Special items with limited availability")
        info_label.setStyleSheet(XcomStyle.label_style())
        layout.addWidget(info_label)
        
        # Black market list
        self.black_market_list = QListWidget()
        self.black_market_list.setStyleSheet(XcomStyle.list_widget_style())
        layout.addWidget(self.black_market_list)
        
        # Purchase controls for black market
        controls = QHBoxLayout()
        
        self.bm_quantity_spin = QSpinBox()
        self.bm_quantity_spin.setMinimum(1)
        self.bm_quantity_spin.setMaximum(10)
        controls.addWidget(QLabel("Quantity:"))
        controls.addWidget(self.bm_quantity_spin)
        
        self.bm_purchase_button = QPushButton("Purchase from Black Market")
        self.bm_purchase_button.setStyleSheet(XcomStyle.button_style())
        self.bm_purchase_button.clicked.connect(self._make_black_market_purchase)
        controls.addWidget(self.bm_purchase_button)
        
        layout.addLayout(controls)
        
        return widget
    
    def _create_orders_tab(self):
        """Create tab for viewing active orders."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Active orders list
        orders_label = QLabel("Active Purchase Orders")
        orders_label.setStyleSheet(XcomStyle.label_style())
        layout.addWidget(orders_label)
        
        self.orders_list = QListWidget()
        self.orders_list.setStyleSheet(XcomStyle.list_widget_style())
        layout.addWidget(self.orders_list)
        
        # Cancel order button
        cancel_button = QPushButton("Cancel Selected Order")
        cancel_button.setStyleSheet(XcomStyle.button_style())
        cancel_button.clicked.connect(self._cancel_order)
        layout.addWidget(cancel_button)
        
        return widget
    
    def _refresh_data(self):
        """Refresh all data displays."""
        self._update_base_info()
        self._update_purchase_list()
        self._update_black_market_list()
        self._update_orders_list()
    
    def _update_base_info(self):
        """Update base and budget information."""
        from ..engine.game import TGame
        game = TGame()
        
        self.current_base = game.get_active_base()
        if self.current_base:
            self.base_label.setText(f"Base: {self.current_base.name}")
        else:
            self.base_label.setText("Base: Not Selected")
        
        self.budget_label.setText(f"Budget: ${game.budget:,}")
        self.purchase_system = game.get_purchase_system()
    
    def _update_purchase_list(self):
        """Update the list of available purchases."""
        self.purchase_list.clear()
        
        if not self.purchase_system or not self.current_base:
            return
        
        # Get available technologies and services for this base
        available_tech = []  # TODO: Get from research system
        available_services = []  # TODO: Get from base facilities
        available_money = 1000000  # TODO: Get from game budget
        
        available_purchases = self.purchase_system.get_available_purchases(
            self.current_base.name, available_tech, available_services, available_money
        )
        
        for entry in available_purchases:
            item = QListWidgetItem(f"{entry.name} - ${entry.cost:,}")
            item.setData(Qt.UserRole, entry)
            self.purchase_list.addItem(item)
    
    def _update_black_market_list(self):
        """Update black market items."""
        self.black_market_list.clear()
        
        if not self.purchase_system:
            return
        
        # TODO: Implement black market listing
        placeholder = QListWidgetItem("Black Market functionality coming soon...")
        self.black_market_list.addItem(placeholder)
    
    def _update_orders_list(self):
        """Update active orders list."""
        self.orders_list.clear()
        
        if not self.purchase_system or not self.current_base:
            return
        
        active_orders = self.purchase_system.get_active_orders(self.current_base.name)
        
        for base_id, orders in active_orders.items():
            for order in orders:
                status_text = f"Order {order.id[:8]} - Status: {order.status}"
                if hasattr(order, 'estimated_delivery'):
                    status_text += f" - ETA: {order.estimated_delivery}"
                
                item = QListWidgetItem(status_text)
                item.setData(Qt.UserRole, order)
                self.orders_list.addItem(item)
    
    def _filter_purchases(self, category: str):
        """Filter purchases by category."""
        # TODO: Implement category filtering
        self._update_purchase_list()
    
    def _on_purchase_selected(self):
        """Handle purchase selection."""
        current = self.purchase_list.currentItem()
        if not current:
            self.purchase_button.setEnabled(False)
            self.purchase_info.clear()
            return
        
        entry = current.data(Qt.UserRole)
        if entry:
            self.purchase_button.setEnabled(True)
            
            # Display purchase information
            info_text = f"Name: {entry.name}\n"
            info_text += f"Category: {entry.category}\n"
            info_text += f"Cost: ${entry.cost:,}\n"
            info_text += f"Delivery Time: {entry.delivery_time} days\n"
            
            if entry.monthly_limit > 0:
                info_text += f"Monthly Limit: {entry.monthly_limit}\n"
            
            if entry.required_technologies:
                info_text += f"Required Tech: {', '.join(entry.required_technologies)}\n"
            
            if entry.required_services:
                info_text += f"Required Services: {', '.join(entry.required_services)}\n"
            
            self.purchase_info.setText(info_text)
            self._update_total_cost()
    
    def _update_total_cost(self):
        """Update total cost display."""
        current = self.purchase_list.currentItem()
        if not current:
            self.total_cost_label.setText("Total Cost: $0")
            return
        
        entry = current.data(Qt.UserRole)
        if entry:
            quantity = self.quantity_spin.value()
            total = entry.cost * quantity
            self.total_cost_label.setText(f"Total Cost: ${total:,}")
    
    def _make_purchase(self):
        """Make a regular purchase."""
        current = self.purchase_list.currentItem()
        if not current or not self.purchase_system or not self.current_base:
            return
        
        entry = current.data(Qt.UserRole)
        quantity = self.quantity_spin.value()
        
        # TODO: Get real values from game systems
        available_tech = []
        available_services = []
        available_money = 1000000
        
        success, order_id, issues = self.purchase_system.place_order(
            entry.id, self.current_base.name, quantity,
            available_tech, available_services, available_money
        )
        
        if success:
            QMessageBox.information(self, "Purchase Successful", 
                                  f"Order {order_id} placed successfully!")
            self._refresh_data()
        else:
            QMessageBox.warning(self, "Purchase Failed", 
                              f"Purchase failed:\n" + "\n".join(issues))
    
    def _make_black_market_purchase(self):
        """Make a black market purchase."""
        QMessageBox.information(self, "Black Market", 
                              "Black market purchases coming soon!")
    
    def _cancel_order(self):
        """Cancel a selected order."""
        current = self.orders_list.currentItem()
        if not current or not self.purchase_system:
            return
        
        order = current.data(Qt.UserRole)
        if order:
            success = self.purchase_system.cancel_order(order.id)
            if success:
                QMessageBox.information(self, "Order Cancelled", 
                                      f"Order {order.id} cancelled successfully!")
                self._refresh_data()
            else:
                QMessageBox.warning(self, "Cancellation Failed", 
                                  "Cannot cancel this order - it may already be in transit.")
    
    def screen_activated(self):
        """Called when screen becomes active."""
        self._refresh_data()
    
    def screen_deactivated(self):
        """Called when screen becomes inactive."""
        pass
