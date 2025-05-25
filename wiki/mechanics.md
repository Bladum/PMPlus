
# [Battle Mechanics]()

## [Movement]()

- normal tile cost 2 points to move, diagonals cost 3, hard terrain cost more, e.g. sand
- typical human soldier will have speed between 6-12, average 8
- rotation may cost 1 point or nothing but this is 90 degrees
- unit can move 4 times per turn, so 4 AP
- unit move for 14 points far with speed of 7 will cost 2 AP (14 / 7 = 2)
- AP cost is calculated automatically based on speed and range of movement

## [Damage method]()

- weapon have damage method = either POINT or AREA
- it defines how damage is distributed on tile when hit
- so typical AP damage is 10 / 0, which means all is damage to tile it hit
- but grenades have it 1 / 12:2, which means 1 is done on hit and 12 is explosion damage and 2 is drop off
- this will calculate range of explosion (which is 6 tiles)
- weapon always use same damage type for both attacks, but if there is ZERO then it's not executed
- both POINT and AREA damage could be of any type like kinetic, explosive, laser, etc.
- POINT damage is randomized 50% - 150% of base, while AREA damage is kept 100% with drop off

## [Damage types]()

- weapon have damage type e.g. kinetic, laser
- armour have damage type resistance for same values
- damage type is used to calculate how target is resistance to damage type of weapon
- use weapon power, roll random value from 50% to 150% 
- apply armour resistance of target, which means 150% is more damage
- apply armour value by reducing power (N - K)
- remaining part apply either STUN or HURT depends on damage type
- check wounds if damage is bigger than 25% of base health (only HURT)

## [Damage model]()

- damage model defines how damage is distributed on different stats of units when hit
- During damage to unit based on weapon damage type we check how much of damage will STUN or HURT unit
- typically for kinetic is 80 to 20 (hurt to stun) but for other damage it could be different
- for every point of damage check is done, its not fixed split
- in future there might be more damage category like damage to MORALE, ENERGY etc

## [Terrain armour and resistance]()

- damage to terrain is one same way like damage to unit
- damage method is either POINT or AREA
  - POINT damage is when it hit a tile it damages unit -> wall -> object -> item
  - AREA damage is when it hit a tile there is area of damage with drop per tile in all directions

Terrain has armour resistance:
 - this defines per type (metal, wood, brick, stone, earth etc)
 - by default all are assigned to one type, could be configured

Examples
- pistol            3-7 damage
- grenade           12 with 2 drop (12 -> 10 -> 8 -> 6 -> 4 -> 2)
- plasma pistol     11 (6-16)
- sniper rifle      8 (4-12)
- heavy plasma      22 (12-32)

Examples of armours of terrain elements:

| Object       | XCOM | 20% of base |
|--------------|------|-------------|
| metal wall   | 80   | 18          |
| ufo wall     | 100  | 20          |
| metal floor  | 60   | 12          |
| fuel pod     | 30   | 6           |
| nav console  | 40   | 8           |
| ufo chair    | 50   | 10          |
| brick wall   | 25   | 5           |
| door         | 20   | 4           |
| xcom craft   | 255  | 50          |
| base wall    | 80   | 16          |
| wall door    | 60   | 12          |
| dirt         | 100  | 20          |
| wood wall    | 15   | 3           |
| vegetable    | 10   | 2           |
| tree         | 20   | 4           |
| stone wall   | 30   | 6           |
| fence        | 10   | 2           |
| window glass | 15   | 3           |
| metal fence  | 20   | 4           |
| wood stuff   | 15   | 3           |
| small plant  | 10   | 2           |
| high terrain | 30   | 6           |
| rock         | 40   | 8           |
| hard rock    | 60   | 12          |
| soft rock    | 50   | 10          |

## [Reaction fire]()

- turn on overwatch for your soldier by spending 1 AP
- remain AP will be used for reaction fire during enemy turn
- moving out of overwatch will cancel it, will cost 1 AP
- if enemy unit will be in sight of your soldier then perform reaction stat test and if pass then fire a shot

## [Psionic]()

- psionics are normal items (in build or not) that perform some psionic action
  - stun             damage unit STUN
  - teleport         move unit
  - mind control     change side of unit
  - panic            damage morale
  - telekinesis      move objects
  - telepathy        show terrain under fog of war
  - start fire       start fire on tile

How to get there?
- first we need to perform some research
- then we need to capture some items
- then we need to build a facility with service to provide a psionic training
- then we need to train units to use it ( either as transformation or promotion )
- then we can use psionic items in battle

- there might be other similar to psionic mechanics like PRIEST
- it can all be done by assigning special skill to unit, then limit use of items to this skill

## [Morale]()

- under stress unit will perform a WILL test 
- test is always with min 10% and max 90% value
- if unit fail then it will lose 1 morale
- morale is recovered after battle to max
- morale is recovered normally 1 per turn if REST is used
- some actions may cause several morale tests

Morale impact is same as sanity but for this battle only:
 - >= 10 -> +1 AP
 - <= 3 -> -1 AP
 - <= 2 -> -2 AP
 - <= 1 -> -3 AP
 - <= 0 -> -4 AP and start to panic

### [Morale loss cases]()

Situation that unit make a test of bravery:
- unit saw friendly unit die (sight)
- unit hear friendly unit die (sense)
- unit got hit even without lose of HP
- got HURT, every 3 HP -> one morale test
- unit got wounded (as a skill wound)
- unit got attacked by enemy reaction fire
- unit saw enemy unit that cause fear
- unit got attacked by enemy that was NOT in sight or sense before end of turn
- unit got suppression by enemy unit

### [Enemy surrender]()

- units may panic due to low morale
- it units already panicked then it may surrender
- as morale gradually increase WHEN rest then it may come back and stop panic
- someone else might help unit to increase morale
- when unit panicked due to morale but then increase morale it is not considered panicked
- if all units are 
  - alive, not killed, not stunned 
  - panicked 
  - then enemy will surrender

### [Panic mode]()

- when low morale unit starts to lose AP
- when morale is 0 or low it has no more AP and starts to panic 
- so panic mode starts with 0 morale or low
- in panic mode if unit when does nothing it regains 1 morale point per turn
- morale may drop below 0 only for the purpose of how long panic may be
- during panic mode unit will randomly, instead of normal action:
  - move (no morale) 
  - use item randomly (no morale) 
  - wait (this will increase morale by 1)
  - drop weapon (no morale)

## [Sanity]()

- damage to sanity is applied only at the end of mission, not during
  - low mission -1
  - med mission -2
  - high mission -3
- sanity is recovered normally 1 per week
- some facilities may improve this rate
- this may be linked to race (sanity recovery)
- sanity does not change during battle, its only for geo game

- Sanity impact:
 - >= 10 -> +1 AP
 - <= 3 -> -1 AP
 - <= 2 -> -2 AP
 - <= 1 -> -3 AP
 - <= 0 -> -4 AP

## [Smoke and fire]()

- battle tile may have either smoke or fire or something else gas ??

Smoke:
   - limit sight by 4 points
   - does not affect fire or movement
   - be inside smoke without armour will inflict 1 damage to STUN per turn

Fire:
  - limit sight by 3 points
  - does not affect fire or movement
  - when on fire tile it will inflict 
    - 1 damage HURT per turn
    - 2 damage to MORALE per turn
    - will put unit on fire status

Status on fire:
  - chance 25% to selfextinguish fire
  - lose 1 HP per turn
  - lose 1 AP 

## [Line of sight]()

- game use concept of fog of war from RTS games, rather than lightning from xcom
- which means that unit can see in range either day / night and tile color is not impacted by source of light
- if you move your unit it will update the visible part of FOG OF WAR
- entire battle scene is colored a bit for night missions but in general no lighting 
- game has 2 level fog of war like in RTS so if your unit sees something, it will be visible under FOG
- Mission underground are considered to be at night but this is defined on map level
  - xcom base is day but underground
  - alien base is night but underground

#### [Types of visibility]()

- sight is used to show terrain in front of unit (standard is 20 and 10 tiles for day/night)
- sense is used to show terrain around unit (standard is 2 tiles) in all directions
- cover on other unit can reduce sight / sense effectively

#### [what can impact field of view ?]()

- basic race sight or sense
- armour type (e.g. heavy armour can limit sense at all to zero)
- ranks (e.g. scout class can increase sight by 3)
- items (e.g. motion scanner can increase sense by 10)

#### [How flares works ?]()

- in general flare would be a short range, short live source of FOV, it will uncover a bit under fog of war
- having flare / flashlight as secondary weapon may also increase sight range to min value of e.g. 13

#### [How visibility is calculated on terrain ?]()

- in open space each tile cost exactly 1 point for calculation of sight
- for day / night there is no difference as unit has different values (20 / 10) but cost on terrain is same
- smoke will block sight by factor of 3
- fire will block sight by factor of 5 
- some semitransparent objects like window, bushes etc may block by 2-3

If you cannot see something you want be able to fire at it (or penalty of 50% is applied)

## [Line of fire]()

- game does not have any LOFT logic like XCOM, no 3D engine inside
- all maps are flat and trajectory of bullets is straight line from middle of tile to middle of tile
- to calculate line of fire a line from source to target is draw
- if it hits any tile with
  - air, it blocks nothing, cost exactly 1 tile, it will not hit this place
  - wall, it blocks everything, cost all, nothing fire be seen further, for sure it will hit here OR before
  - objects semi-transparent or with holes, like fence, window, plants it may have a chance to block some %
  - this works same way like line of sight, it will reduce chance to hit

Example:
- soldier with 80% acc with Rifle 70% fire at target through fence (30% block)
- base to hit = 56% is reduced on this tyle by 56% * 70% = 39%
- but this is only simulation, actual fire is done another way

#### [Chance to hit target simulation]()

To calculate chance to hit a target :
- basic soldier accuracy, include if is crouching, is moving and is hurt
- weapon accuracy 
- size of target 
- reaction (dodge) chance of target (reaction * move left mod * health left mod * armour mod)
- current range / max range of weapon 
- if you actually see the target tile
- cover
  - this is calculated by all tiles that are from source to target
  - so 3 tiles by 10% cover givers 90% * 90% * 90% = 73% of chance to hit mod

If unit decide to fire at this place then roll is made vs this value chance to hit

#### [Chance to hit target execution]()

- if unit pass to hit check then bullet goes directly to target tile
- if unit fail to hit check then new target tile is calculated
  - calculate R = distance to target / max weapon range
  - find new target tile which is in R tiles from original
  - if its the same as target, repeat
- from source to target tile draw a line 
- and check each tile for actual hit, checking its block chance (e.g. fence has 30%, air has 0%, wall has 100%)
- if it hits tile, then execute damage method

## [Action points]()

- each unit has speed from 6 to 12 for human, typically 8, this defines only movement
- movement cost 2 point on normal tile, more on hard tile
- movement cost 3 when moving diagonally (always 50% more)
- rotation cost is 1 per 90 degrees

#### [Unit has 4 AP to spent on:]()
  - move
  - cover (aka crouch / kneel)
  - overwatch (aka reaction fire)
  - use item (shoot, throw, use)
  - rest
  - throw item (primary / secondary)
  - suppress enemy ( to agreed )

#### [What can impact action points ?]()
  - in general its all 4 AP
  - some effects like BERZERK may increase AP +1
  - some effects like PANIC may decrease AP -1

#### [Example use cost:]()
  - pistol 1
  - knife 1
  - rifle 2
  - grenade 2
  - shotgun 2
  - smg 2
  - sniper 3
  - rocket launcher 4
  - mortar 4
  - medikit 2
  - flare 1 
  - motion scanner 1
  - healing gel 1
  - machine gun 4
  - grenade launcher 3
  - psi amp 2
  - stun rod 1
  - laser sword 2
  - heavy axe 3

## [Unit Wounds]()

- there is no concept of bleeding if you got hit you got wounds
- instead for every high damage hit you get a chance to get a "wound"
  - below 25% of base health = nothing of wound
  - 25-50% of base health = 25% chance of wound
  - 50%-75% of base health = 50% chance of wound
  - 75%-100% of base health = 75% chance of wound
- of course if you hit for max damage unit dies :) 
- stun damage does not count here, its only hurt damage
- wounds are permanent and may cause unit to be crippled (check ranks section)
- unit can be healed via medikit during battle to MAX but still will get wound
- it is assumed that wounds cannot be healed during battle, only after (thou health can be to max)
- wound can be losing an eye, broken arm, lose leg etc...

concept behind it:
- health is ability to fight, not exactly your health. If you have 2 of 12 you still can, thou limited to fight
- wounds is your "experience" from battlefield and should be permanent

## [Throwing]()

- in general there is nothing to throw
- grenades are used like weapons with specific stats to grenades
- units cannot throw random items around
- if unit fire item that supposed to create something on a tile e.g. flare effect it creates OBJECT
- aim STAT is used for all throwing / firing activities
- strength STAT might be used to define range of throwing instead of actual item range 

Range of throwing:
- some method (strength / weight)
- this is used instead of actual item range

TODO proximity grenades to be agreed how to do, so they do explode after some time

## [Night mission]()

- game has day / night cycle on world map 
- there is either day or night mission, there is nothing in between
- underground missions are always night, unless mission said so (like XCOM base)
- game does not have lighting like in XCOM, rather it has fog of war like RTS game
- unit once move it unhide fog of war, but still must be to visible units / objects in tile 
- flares are used to create light in tile but with ver limited range (2-3) and time (4-6 turns)
- flashlights may improve visibility in night but not in day when use as secondary item

## [Alien movement]()

- map blocks have nodes, which are used by AI to control its movement
- AI nodes have value that would control weight for AI, 
- AI nodes are connected to other nodes, also outside of this map block
- 

## [Medikit]()

- medikit is used to heal and restore health
- wounds must be healed in hospital / base, not on battle field
- medikit can be applied self (1 HP) or another unit (2-5 HP)
- it may be limited to more advanced units with skill Medic

### [Motion scanner]()

- it add sense stat to unit so it can detect units around

## [Scout & Sniper]()

- one unit can swipe map and detect enemies
- another unit can fire at it but with penalty of 50%

### [Soldier actions during battle]()

Use:
  - use primary or secondary items

Overwatch action:
  - move unit into watching mode, it will use remaining AP to fire at enemy

Cover action:
  - move unit into cover mode, it will focus on better AIM and become smaller target

Rest action: 
  - spent AP to recover energy / morale

Move action: 
  - spent AP to move unit, move range is based on unit speed
  - typical unit with speed 8 can move 4 tiles per 1 AP, and 16 tiles per turn for all AP
  - game will automatically calculate action points used, based on 
    - total cost to move to this place (2 TU per tile, 3 diagonal, some terrains x2) => 17
    - rotation by 90 degrees (1 TU per 90 degrees) => 1
    - unit speed e.g. 8
    - this will cost 17/8 = 2.125 AP

Stealth move action:
  - spent 2 AP to move unit just like move action but WILL NOT trigger reaction fire from enemy

Suppress action:
  - try to aim at enemy but do not fire, it will something limit enemy AP next turn


### [High terrain on battlefield]()

- maps are flat but some terrain like natural terrain which is NOT wall may have height
- there is normal / high terrain profile
- this may be used to get some cover or to get some bonus
- to get on high terrain you need to spent x2 movement points
- difference between this and WALL is that in general WALL blocks movement, while FLOOR does not

#### [Impact on high terrain]()

- slower movement going UP or DOWN slope
- when on high terrain then get sight / range bonus +2 / +1 and do not block another high ground
- when on low terrain then cost to see through is higher x4
- when fire from low terrain vs high terrain or via slop then block 25%
- two tiles of slope assume its terrain 2 level high
- game should up front calculate this and store it in map
