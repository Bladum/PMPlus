
# [Sounds]()

- TODO


# [Graphics]()

- no animations in general, unless its a smoke / fire etc
- some units might have up to 4 sprites for animation, like in rouge like
- unit attacks just display a short animation of attack in place where it happens, color depends on damage type
- no need to display bullet trace, or it could just be a line
- in general when something fired it may unhide fog of war in this place like in RTS

World map
- each tile is small only 8x8 pixel with all icons are 6x6 for bases, crafts etc
- each tile is 500km, so entire world is 90x45 tiles

Battle scape
- each tile is 32x32 pixels, with map blocks 15x15 tiles and battle is up to 7x7 map blocks
- tiles are drown from top down, like Rusted Warfare
- some elements might be draw from side to better represent them, like furniture

Units:
- unit is either small 32x32 or large with 2x2 tiles (64x64)
- each unit is drawn from top down in one direction
- unit also has corpse image when dead
- game rotates units by 90 deg when needed (4 sides)
- unit has several sprites based on its elements
  - main body and head based on RACE
  - armour based on ARMOUR
  - left / right hand would be primary / secondary weapon
  - legs are based on RACE and used to animate when moving
  - head is based on random face only for selected races, like sectoid might have different heads

Base scape
- each facility is 32x32 pixels and base is max size of 5x5 facilities in single base
