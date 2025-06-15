# GUI Base Screens

This folder contains the main GUI screen classes for the XCOM base management interface. Each class represents a different screen or panel in the base UI, such as Barracks, Hangar, Storage, and more.

## Classes

### TGuiBaseTopPanel
Widget for managing the top navigation panel of the XCOM inventory interface. Provides screen switching, base selection, and displays current base, date, and funds.

### TGuiBarracks
Main barracks management screen with unit roster, equipment loadouts, and inventory functionality.

### TGuiHangar
Screen for craft management in the base.

### TGuiStorage
Screen for base storage management.

### TGuiTransfer
Screen for inter-base transfers.

### TGuiPrison
Screen for containment/prison management.

### TGuiAcademy
Screen for manufacturing and training management.

### TGuiWorkshop
Screen for manufacturing management.

### TGuiLab
Screen for science and research management.

### TGuiMarket
Screen for purchases and market management.

### TGuiArchive
Screen for research and records management.

### TGuiBaseInfo
Screen for base info summary and activities overview.

### TGuiFacility
Screen for facility management.

### TPurchaseGui
Purchase system interface for buying items, units, and crafts.

---

All classes inherit from `TGuiCoreScreen` unless otherwise noted. See also: `wiki/gui.md` for more details on the GUI system.
