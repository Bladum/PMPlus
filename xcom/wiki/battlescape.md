

# [Battlescape]()

### [Map script]()

- method how to generate map
- usually it starts with add UFO, add CRAFT and then fill the rest
- but some missions might be different

### [Map sizes]()

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
- neutral, just wondering, try to protect it self

### [High terrain on battlefield]()

- maps are flat but some terrain like natural terrain which is NOT wall may have height
- there is normal / high terrain profile
- this may be used to get some cover or to get some bonus
- to get on high terrain you need to spent x2 movement points
- difference between this and WALL is that in general WALL blocks movement, while FLOOR does not

Bonus on high terrain:
- +2 / +1 to sight
- if fight HTH with someone who is on normal terrain then +10% to hit


TODO agreed rules about it

### [Complex maps]()

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

### Terrains

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
  - order overylay

- tile graphics are not autotiles, they must be added manually
- tile graphics are not animated, they are static
