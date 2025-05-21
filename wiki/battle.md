

# [Battlescape]()

### [Battle script]()

- method how to generate map
- usually it starts with add UFO, add CRAFT and then fill the rest
- but some missions might be different

### [Battle sizes]()

Battle maps are in size
- micro 3x3 = 9
- small 4x4 = 16
- medium 5x5 = 25
- large 6x6 = 36
- huge 7x7 = 49

### [Battle sides]()

There are always 4 sides:
- xcom player
- alien / cults as enemy
- optional ally with xcom, fights with aliens, does not protect neutral
- neutral, just wondering, try to protect itself




### [Multilevel maps]()

- in general maps are FLAT but are larger
- each map could be multilevel, but this works like in falluot game underground base
- one level is completely different from another, cannot interact other than teleport
- units can move from one level to another via e.g. elevator / portal 
- each level can be generated from different set of tiles or the same

### [Map blocks]()

- are build from battle tiles 15x15 or bigger (30x30, 45x45 etc)
- some map blocks can be mirrored or rotated before put into the map as graphics design allows to do it
- map blocks are FLAT, there are no multilevel map blocks
- map blocks are build in TILED editor

### [Terrains]()

- Terrain just keeps list of potential map blocks to generate battle map out of it
- many terrains are not linked with a biome on world map
- every ufo and xcom craft must also have terrain, which in many cases is just one map block
- terrain also has a map script that defines how 
- each terrain has single map tileset

### [Map tileset]()

- single terrain type has single file and png image that represents terrains
- 

### [Map tiles]()

each tile contains:
  - floor - normal walk
  - wall - block walk. This is for both walls and objects like barrel
  - object - something to pick up, normal walk (corpes, flares, grenades)
  - unit
  - effect e.g. smoke
  - fog of war overlay
  - order overlay

- tile graphics are not auto tiles, they must be added manually
- tile graphics are not animated, they are static

### [Post battle report]()

- earn experience for units
- convert all live units into capture items
- collect all objects on ground as items
- calculate wounds on units
- pay for ammo for all weapons (reload)
- pay for salary for all soldiers (salary or repairs)
- total score for XCOM
- report medals for mission
- convert other items into money

### [User interaction on map]()

- mouse wheel -> zoom
- LMB
  - on unit to select
  - on tile to move
  - with shift on tile to run
  - with ctrl on tile to sneak
- RMB
  - on tile to rotate to this place
  - with alt to throw item to this place
  - with shift to suppress this tile
  - with control to fire to this place



### [Battle Mission Objectives]()

- in general each mission has a score based on 
  - enemy captured units >0
  - enemy killed units >0
  - neutral units killed <0
  - neutral units survived >0
  - your units killed <0 
  - captured items >0
  - destroyed items <0
- mission may have objective that is not related to score from units
  - if you complete this objective then you get score
  - if you fail complete this objective then you lose this score
- this means you might have mission with negative score from killed civilians
- but you get the objective (e.g. kill enemy boss) then you get this score
- so one thing is when battle is over, and the other thing is when you get score for objective
- mission might have many objective, if all are fulfilled then its over
- mission is always over when all units are dead or surrender

### [Battle Mission Objectives]()

#### Core Objectives
- Eliminate - Defeat all enemy units (default objective)
- Escape - Move all units to extraction point

#### Time-Limited Objectives
- Hold - Survive for specified number of turns
- Blitz - Eliminate all enemies before time limit expires

#### Territory Objectives
- Defend - Prevent enemies from capturing marked POC
- Conquer - Conquer marked POC from enemy forces
- Explore - Reveal specified percentage of the map

#### Unit-Based Objectives
- Rescue - Locate friendly units and escort them to extraction point
- Capture - Capture alive specific units
- Hunt - Eliminate specific units
- Recon - Identify/mark specific enemy units without engaging
- Protect - Ensure specific units survive the mission

#### Object-Based Objectives
- Sabotage - Destroy designated objects
- Retrieve - Collect designated object

### Suggested Additional Objectives
- Escort - Protect moving target as it travels across the map
- Ambush - Set up position and eliminate enemy patrol/convoy
