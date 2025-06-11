# GUI Base Screens

This folder contains the main GUI screen classes for the XCOM base management interface. Each class represents a different screen or panel in the base UI, such as Barracks, Hangar, Storage, and more.

## Classes

### TGuiBaseTopPanel
Widget for managing the top navigation panel of the XCOM inventory interface. Provides screen switching, base selection, and displays current base, date, and funds.
- **Attributes:** current_screen, available_screens, screen_buttons, base_buttons, base_info_label, date_label, money_label
- **Methods:** get_current_screen(), set_screen(), update_date_display(), update_money_display(), _setup_ui(), _create_screen_buttons(), _create_base_buttons(), _create_info_labels(), _handle_screen_button_click(), _handle_base_button_click(), _switch_base(), _update_base_display()

### TGuiBarracks
TGuiBarracks implements the barracks management screen with unit roster, equipment loadouts, and inventory functionality.
- **Purpose:** Provides the main interface for managing units, their equipment, loadout templates, and stats in the base barracks.
- **Attributes:**
  - game: Reference to the main game instance
  - unit_inventory_manager: Manager for unit inventory operations
  - current_unit: Currently selected unit name
  - equipment_slots: List of equipment slot widgets
  - item_list_widget: Widget displaying available items
  - unit_list_widget: Widget displaying available units
  - weight_label: Label showing equipment weight
  - unit_info_label: Label showing unit information
  - load_template_button: Button for loading equipment templates
  - summary_label: Label showing barracks summary information
  - stat_bars: Progress bars for unit stats
  - traits_layout: Layout for displaying unit traits
  - unit_avatar_label: Label for unit avatar
- **Methods:**
  - screen_activated(), screen_deactivated(), refresh_base_data(), update_summary_display(), _on_unit_selected(), _update_unit_stats(), _update_unit_traits(), _save_template(), _load_template(), _new_template(), _rename_template(), _delete_template(), _on_template_selected(), _update_unit_equipment_status(), _display_unit_avatar(), _setup_ui(), _setup_equipment_slots(), _setup_template_controls(), _setup_weight_label(), _setup_unit_avatar(), _setup_summary_box(), _setup_unit_list(), _setup_item_list(), _setup_stats_box(), _setup_traits_box(), _setup_fire_button(), _setup_basic_info_box(), _finalize_ui_setup(), _update_weight_display(), _update_equipment_slot_states(), _calculate_combat_effectiveness(), _test_equipment_slots(), _adjust_color()

### TGuiHangar, TGuiStorage, TGuiTransfer, TGuiPrison, TGuiAcademy, TGuiWorkshop, TGuiLab, TGuiMarket, TGuiArchive, TGuiBaseInfo, TGuiFacility
Stub classes for other base screens. Each inherits from TGuiCoreScreen and represents a different aspect of base management (crafts, storage, transfers, etc.).

---

See also: `wiki/gui.md` for more details on the GUI system.
