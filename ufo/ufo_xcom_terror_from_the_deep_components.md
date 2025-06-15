# X-COM: Terror from the Deep — Comprehensive System & Feature Reference

This document provides a detailed reference for all major and minor systems, mechanics, and content in X-COM: Terror from the Deep, following the structure of the original UFO: Enemy Unknown documentation for clarity and comparison.

---

## Lore & Story Overview
It is 2040, decades after X-COM defeated the alien threat from Mars. Humanity has rebuilt, but a new terror emerges from the depths of Earth’s oceans. Ancient alien forces, awakened by the destruction of the Martian Brain, begin a campaign of terror against coastal cities and shipping. These aquatic aliens, led by the ancient alien entity T’leth, seek to reclaim the planet and enslave humanity. X-COM is reactivated as an underwater defense force, tasked with fighting the alien menace, uncovering their secrets, and ultimately launching a final assault on the alien city beneath the sea to save Earth once again.

---

## Table of Contents
1. Game Structure & Flow
2. Geoscape (Strategic Layer)
3. Base Management
4. Facilities (Base Modules)
5. Personnel Management
6. Research & Technology Tree
7. Manufacturing (Engineering)
8. Interception & Air Combat
9. Battlescape (Tactical Combat)
10. Aquanauts: Stats, Progression, and Morale
11. Aliens: Races, Behavior, and Missions
12. Alien Subs: Types, Layouts, and Missions
13. Equipment, Weapons, and Inventory
14. Economy, Funding, and World Relations
15. Victory, Defeat, and Endgame
16. User Interface & Quality of Life
17. Miscellaneous Features
18. References

---

## 1. Game Structure & Flow
### Dual-Layer Gameplay
- **Geoscape:**
  - Real-time global strategy, underwater base/resource management, event response.
  - Time management, detection, interception, and resource allocation.
- **Battlescape:**
  - Turn-based tactical combat, squad-level control, destructible underwater environments.
  - Mission objectives: eliminate/capture aliens, rescue civilians, recover artifacts.

### Progression
- **Research-driven:** Unlock new tech, subs, and story progression via research.
- **Base Expansion:** Build new underwater bases for coverage, redundancy, and specialization.
- **Alien Escalation:** Aliens increase mission frequency, tech, and aggression over time.

### Permadeath & Persistence
- **Permanent Loss:** Aquanauts, equipment, and resources lost in combat are gone forever.
- **Veteran Value:** Surviving aquanauts gain experience and become valuable assets.

### Difficulty Levels
- **Beginner, Experienced, Veteran, Genius, Superhuman:**
  - Affect alien stats, mission frequency, aggression, and funding.
  - Higher levels: more aliens, tougher AI, less forgiving economy.

### Save/Load System
- **Manual & Auto-Save:**
  - Save at any time in Geoscape or Battlescape.
  - Multiple slots for experimentation and recovery.

---

## 2. Geoscape (Strategic Layer)
- **World Map:**
  - Global oceanic map with bases, subs, alien subs, alien colonies, and mission sites.
  - Day/night cycle affects detection and tactical missions (night missions are harder).
- **Time Controls:**
  - 5s, 1min, 5min, 30min, 1hr, 1day increments; pause/resume.
- **Event System:**
  - Alien sub sightings, terror attacks, alien colonies, funding changes, research/manufacturing completion, personnel arrivals, base construction.
- **Base Placement:**
  - Player chooses initial underwater base location; can build up to 8 bases worldwide.
- **Mission Generation:**
  - Random and scripted events (alien subs, terror sites, alien colonies, retaliation, infiltration).
- **Funding Nations & Relations:**
  - 16 nations provide monthly funding; can increase, decrease, or withdraw support.

---

## 3. Base Management
- **Facilities:**
  - Living Quarters, Laboratories, Workshops, Stores, Sub Pens, Sonar, Missile/Particle/Plasma Defenses, Alien Containment, MC Lab, General Stores, Transmission Resolver, Magnetic Ion Shield.
- **Construction:**
  - Facilities are built on a grid, take time and money, and must be connected to the access lift.
- **Base Defense:**
  - Alien attacks trigger base defense missions; base layout affects tactical map.
- **Resource Storage:**
  - Stores for equipment, alien artifacts, Zrbite, and corpses.
- **Personnel & Sub Management:**
  - Assign aquanauts, scientists, engineers, and subs to bases.
- **Transfers:**
  - Move personnel, equipment, and subs between bases (with transfer time).

---

## 4. Facilities (Base Modules)
| Facility              | Function                                      | Capacity/Effect                | Build Time | Cost     |
|-----------------------|-----------------------------------------------|-------------------------------|------------|----------|
| Access Lift           | Entry/exit for personnel/aliens               | 1 per base                    | 6 days     | $350,000 |
| Living Quarters       | Houses personnel                              | 50 per module                 | 16 days    | $450,000 |
| Laboratory            | Research projects                             | 50 scientists per lab         | 26 days    | $850,000 |
| Workshop              | Manufacturing projects                        | 50 engineers per workshop     | 32 days    | $900,000 |
| General Stores        | Stores all items and artifacts                | 50 units per module           | 10 days    | $200,000 |
| Sub Pen               | Houses one sub                                | 1 sub per pen                 | 25 days    | $250,000 |
| Small Sonar           | Detects alien subs (short range)              | 10%/30min, 3000nm             | 12 days    | $600,000 |
| Large Sonar           | Detects alien subs (long range)               | 20%/30min, 4500nm             | 25 days    | $1,200,000 |
| Missile Defenses      | Automated base defense                        | 20 damage per module          | 12 days    | $250,000 |
| Particle Defenses     | Improved base defense                         | 70 damage per module          | 18 days    | $900,000 |
| Sonic Defenses        | Advanced base defense                         | 140 damage per module         | 22 days    | $1,400,000 |
| Magnetic Ion Shield   | Repels attacking alien subs, increases defense| +50% defense, delays entry    | 25 days    | $900,000 |
| Alien Containment     | Holds live aliens for research                | 10 aliens per module          | 18 days    | $450,000 |
| MC Lab                | Trains aquanauts in molecular control         | 10 aquanauts per lab/month    | 30 days    | $850,000 |
| Transmission Resolver | Perfect alien sub detection, mission/race info| 100% detection, all info      | 30 days    | $1,400,000 |

- **Facility Upkeep:** Each facility has a monthly maintenance cost.
- **Destruction:** Destroyed facilities (in base defense) are lost and must be rebuilt.

---

## 5. Personnel Management
- **Aquanauts:**
  - Recruit, assign to squads, equip, and transfer. Each has unique stats and names.
  - Can be assigned to subs for missions.
- **Scientists:**
  - Hire and assign to research projects; more scientists = faster research.
- **Engineers:**
  - Hire and assign to manufacturing projects; more engineers = faster production.
- **Hiring/Firing:**
  - Hire or sack staff; costs money and time.
- **Transfers:**
  - Move personnel, equipment, and subs between bases (with transfer time).
- **Arrival Delays:**
  - New hires and transfers take time to arrive at their destination.

---

## 6. Research & Technology Tree
- **Research Topics:**
  - Alien corpses, live aliens, alien sub components, alien weapons, armor, subs, MC tech, and story-critical tech.
- **Dependencies:**
  - Some topics require prior research or captured aliens.
- **Alien Interrogation:**
  - Captured aliens unlock unique research (e.g., alien missions, MC tech, T’leth location).
- **Research Output:**
  - Unlocks new equipment, subs, facilities, and the final mission.
- **Research Management:**
  - Assign scientists, manage priorities, and monitor progress.
- **Research Speed:**
  - Determined by number of scientists and project complexity.
- **X-COMpediA:**
  - In-game encyclopedia updated with each completed research topic.

---

## 7. Manufacturing (Engineering)
- **Production Queue:**
  - Select items to manufacture; assign engineers and allocate resources.
- **Resource Requirements:**
  - Some items require alien alloys (Aqua Plastics), Zrbite, or other recovered materials.
- **Production Time & Cost:**
  - Each item has a build time and cost per unit.
- **Selling:**
  - Manufactured and recovered items can be sold for profit (except Zrbite and alien corpses).
- **Manufacturing Management:**
  - Assign engineers, manage priorities, and monitor progress.

---

## 8. Interception & Air Combat
- **Sub Types:**
  - Barracuda (Fighter), Triton (Transport), Hammerhead, Manta, Leviathan (advanced alien-tech subs).
- **Loadout:**
  - Equip subs with weapons (torpedoes, gas cannons, sonic oscillators, PWT launchers).
- **Detection:**
  - Sonar range and detection chance; Transmission Resolver for perfect detection.
- **Sub Combat UI:**
  - Real-time minigame: approach, engage, disengage, use weapons, or retreat.
- **Alien Sub Crash/Landing:**
  - Downed or landed alien subs generate ground missions.
- **Sub Damage & Repair:**
  - Damaged subs require time to repair in sub pens.
- **Fuel & Ammo:**
  - Subs consume fuel and ammunition; must return to base to refuel/rearm.

---

## 9. Battlescape (Tactical Combat)
- **Mission Types:**
  - Alien Sub Recovery, Alien Sub Landing, Port Attack, Shipping Route, Base Defense, Alien Colony Assault, T’leth Final Mission.
- **Turn-Based System:**
  - Each side takes turns; aquanauts have Time Units (TUs) for actions.
- **Actions:**
  - Move, kneel, fire (snap, aimed, auto), throw, reload, use items, open doors, pick up/drop items.
- **Fog of War:**
  - Limited vision; line-of-sight and night missions (use flares).
- **Destructible Environment:**
  - Buildings, terrain, and alien subs can be destroyed.
- **Morale & Panic:**
  - Low morale can cause panic or berserk behavior.
- **Civilians:**
  - Present in port/shipping missions; can be killed or saved.
- **Victory/Defeat:**
  - Win by eliminating/capturing all aliens; lose if all aquanauts are killed or withdraw.
- **Loot & Recovery:**
  - Surviving aquanauts and recovered items return to base.
- **Environmental Hazards:**
  - Fire, smoke, explosions, and terrain hazards affect combat.
- **AI Behavior:**
  - Aliens use cover, patrol, ambush, and use MC attacks.
- **Opportunity Fire (Reaction Shots):**
  - Units with unspent TUs may fire during the enemy turn if a hostile is spotted.
- **Wounds & Bleeding:**
  - Aquanauts can suffer wounds that cause bleeding each turn; medikits can stop bleeding.
- **Unconsciousness:**
  - Aquanauts and aliens can be knocked unconscious (stun damage); may recover during mission.

---

## 10. Aquanauts: Stats, Progression, and Morale
- **Attributes:**
  - Time Units, Stamina, Health, Strength, Firing Accuracy, Throwing Accuracy, Bravery, Reactions, MC Strength, MC Skill, Rank.
- **Experience:**
  - Stats improve with use (e.g., firing increases accuracy, MC use increases MC skill).
- **Ranks:**
  - Rookie, Squadie, Sergeant, Captain, Commander; higher ranks boost squad morale.
- **Wounds & Death:**
  - Wounded aquanauts require recovery time; dead aquanauts are lost permanently.
- **Morale System:**
  - Affected by casualties, alien attacks, and mission events.
- **Molecular Control (MC):**
  - MC Lab training unlocks MC attacks (panic, mind control) for aquanauts with sufficient MC strength.
- **Medals & Promotions:**
  - Aquanauts are promoted based on performance and squad composition.
- **Fatigue:**
  - Stamina is consumed by movement and actions; low stamina reduces TUs.

---

## 11. Aliens: Races, Behavior, and Missions
- **Alien Races:**
  - Aquatoid, Gillman, Lobsterman, Tasoth, Calcinite, Deep One, Bio-Drone, Tentaculat, Triscene, Hallucinoid, Xarquid.
- **Unique Abilities:**
  - MC attacks (Aquatoid, Tasoth), zombification (Tentaculat), heavy armor (Lobsterman), regeneration (Deep One).
- **Alien Missions:**
  - Abduction, Harvest, Research, Terror, Infiltration, Colony Construction, Retaliation, Supply.
- **AI Behavior:**
  - Patrol, ambush, seek and destroy, defend sub/colony, use of MC.
- **Alien Colonies:**
  - Aliens build hidden colonies; can be discovered and assaulted.
- **Alien Equipment:**
  - Aliens use sonic weapons, grenades, and special items (MC disruptor, thermal shock launcher).
- **Molecular Control:**
  - Some aliens can panic or mind control aquanauts; resistance depends on aquanaut MC strength.

---

## 12. Alien Subs: Types, Layouts, and Missions
- **Alien Sub Types:**
  - Survey Ship, Escort, Cruiser, Hunter, Battleship, Dreadnought, Fleet Supply Cruiser.
- **Roles:**
  - Each sub type is used for specific alien missions and has unique interior layouts.
- **Alien Sub Components:**
  - Power Source, Navigation, Aqua Plastics, Zrbite, Alien Sub Construction, etc.
- **Mission Progression:**
  - Alien subs perform missions on the Geoscape, triggering events and missions.
- **Alien Sub Recovery:**
  - Recovered subs provide research materials and loot.
- **X-COMpediA Entries:**
  - Each sub type and component has a detailed in-game encyclopedia entry.

---

## 13. Equipment, Weapons, and Inventory
- **Weapon Types:**
  - Gauss, Sonic, Disruptor, Torpedo, Thermal Tazer, Vibro Blade, Drill, PWT Launcher.
- **Ammunition:**
  - Standard, high-explosive, stun bombs, Zrbite-based.
- **Armor:**
  - Plastic Aqua Armor, Ion Armor, Magnetic Ion Armor.
- **Special Equipment:**
  - Medikit, Motion Scanner, MC Reader, Dye Grenade, Thermal Shok Launcher.
- **Inventory System:**
  - Aquanauts have hand, belt, backpack, shoulder, and ground slots; weight affects TUs and stamina.
- **Item Recovery:**
  - Only items carried or in the transport at mission end are recovered.
- **Encumbrance:**
  - Carrying too much weight reduces TUs and stamina.
- **Explosives:**
  - Grenades, high-explosive packs, proximity grenades, and torpedoes.
- **Weapon Modes:**
  - Snap shot, aimed shot, auto shot (where available); each with different TU costs and accuracy.
- **Stun & Capture:**
  - Thermal Tazer and Thermal Shok Launcher can incapacitate aliens for capture and research.

---

## 14. Economy, Funding, and World Relations
- **Funding Nations:**
  - 16 nations provide monthly funding; can increase, decrease, or withdraw support.
- **Monthly Reports:**
  - Performance-based funding adjustments; nations may sign pacts with aliens.
- **Income & Expenses:**
  - Funding, sales, and manufacturing vs. salaries, maintenance, construction, and purchases.
- **Black Market:**
  - Sell recovered alien artifacts and manufactured goods for profit.
- **Game Over:**
  - Two consecutive months of negative balance or all nations withdrawing ends the game.
- **Panic & Infiltration:**
  - Nations may panic or sign pacts with aliens if not protected; affects funding and game outcome.

---

## 15. Victory, Defeat, and Endgame
- **Victory:**
  - Research and unlock the T’leth mission; send a squad to the alien city and defeat the alien entity.
- **Defeat:**
  - X-COM is disbanded if funding is lost, all bases are destroyed, or the T’leth mission fails.
- **Multiple Endings:**
  - Victory (Earth saved) or defeat (Earth conquered/flooded).
- **Endgame Sequence:**
  - Final mission at T’leth is a multi-stage tactical battle.

---

## 16. User Interface & Quality of Life
- **X-COMpediA:**
  - In-game encyclopedia with detailed info on all researched items, aliens, and equipment.
- **Save/Load:**
  - Multiple save slots; manual and auto-save.
- **Options:**
  - Difficulty levels, sound/music, controls.
- **Notifications:**
  - Pop-ups for research, manufacturing, alien sub detection, funding changes, and mission events.
- **Graphical UI:**
  - Icon-based, mouse-driven interface; isometric tactical view.
- **Hotkeys:**
  - Keyboard shortcuts for common actions in both Geoscape and Battlescape.
- **Tooltips:**
  - Mouse-over tooltips for UI elements and equipment.

---

## 17. Miscellaneous Features
- **Sound & Music:**
  - Dynamic soundtrack and sound effects for Geoscape, Battlescape, and events.
- **Randomization:**
  - Procedural map generation for tactical missions; random aquanaut stats and names.
- **Localization:**
  - Multiple language support in some versions.
- **Modding & Community:**
  - OpenXcom and other projects have extended/modded the original game.

---

## 18. References
- [Wikipedia: X-COM: Terror from the Deep](https://en.wikipedia.org/wiki/X-COM:_Terror_from_the_Deep)
- [UFOPaedia.org: TFTD](https://www.ufopaedia.org/index.php/X-COM:_Terror_from_the_Deep)
- [StrategyWiki: TFTD](https://strategywiki.org/wiki/X-COM:_Terror_from_the_Deep)

---

*This document is a comprehensive, feature-level and high-level summary for design, analysis, and comparison. For in-depth mechanics, see the referenced wikis and original game manuals.*
