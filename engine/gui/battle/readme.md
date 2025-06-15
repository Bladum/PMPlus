# GUI Battle Screens

This folder contains the main GUI screen classes for the XCOM battle interface. Each class represents a different screen, panel, or visual component used during tactical combat.

## Classes

### BattleInteractionController
Handles user interaction (mouse, wheel, selection, path planning) for the battle map. Connects to BattleMapView and TBattle.

### BattleMapView
Visualizes the battle map and units using QGraphicsView/QGraphicsScene. Handles efficient drawing and updating of tiles and units.

### TGuiBattleInventory
Main GUI screen for battle inventory management.

### TGuiBattleBrief
Main GUI screen for mission briefing.

### TGuiBattleEnd
Main GUI screen for mission end/debriefing.

### UnitGraphicsItem
QGraphicsRectItem subclass for visual representation of a unit on the battle map.

---

All classes inherit from `TGuiCoreScreen` or appropriate Qt base classes. See also: `wiki/gui.md` for more details on the GUI system.
