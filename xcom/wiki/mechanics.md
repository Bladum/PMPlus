
# [Battle Mechanics]()

### [Throwing]()

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

### [Damage calculations]()

- in general each weapon have damage type e.g. kinetic
- but also are two types of damages, ON HIT, IN RANGE
- so typical AP damage is 10 / 0, which means all is damage to tile it hit
- but grenades have it 1 / 12:2, which means 1 is done on hit and 12 is explosion damage and 2 is drop off
- this will calculate range of explosion (which is 6 tiles)
- weapon always use same damage type for both attacks, but if there is ZERO then it's not executed

### [Damage to soldier when hit]()

- take weapon power, roll random value from 50% to 150% with round to power value
- apply armour resistance of target, which means 150% is more damage
- apply armour value by reducing power (N - K)
- remaining part apply either STUN or HURT depends on damage type
- check wounds if damage is bigger then 25% of base health (only HURT)

### [Supporting your units ]()

Some items may allow for skills

Healing
- items like medikit can heal units from short distance (1-2 tiles)
- its a secondary item, it heals HEALTH mainly
- cannot heal wounds on battlefield, only in hospital

Leadership
- some units may have a class that boost other units using a secondary item like banner
- or special items to boost morale or will 



### [Line of sight, Field of view and visibility ]()

- game use concept of fog of war from RTS games, rather than lightning from xcom
- which means that unit can see in range either day / night and tile color is not impacted by source of light
- if you move your unit it will update the visible part of FOG OF WAR
- entire battle scene is colored a bit for night missions but in general no lighting 
- game has 2 level fog of war like in RTS so if your unit sees something, it will be visible under FOG
- Mission underground are considered to be at night but this is defined on map level
  - xcom base is day but underground
  - alien base is night but underground

Types of visibility:
- sight is used to show terrain in front of unit (standard is 20 and 10 tiles for day/night)
- sense is used to show terrain around unit (standard is 2 tiles) in all directions
- TODO more in future

what can impact field of view ?
- basic race sight or sense
- armour type (e.g. heavy armour can limit sense at all to zero)
- classes (e.g. scout class can increase sight by 3)
- items (e.g. motion scanner can increase sense by 10)

How flares works ? 
- in general flare would be a short range, short live source of FOV, it will uncover a bit under fog of war
- having flare / flashlight as secondary weapon may also increase sight range to min value of e.g. 13

How visibility is calculated on terrain ?
- in open space each tile cost exactly 1 point for calculation of sight
- for day / night there is no difference as unit has different values (20 / 10) but cost on terrain is same
- smoke will block sight by factor of 3
- fire will block sight by factor of 5 
- some semitransparent objects like window, bushes etc may block by 2-3

If you cannot see something you want be able to fire at it (or penalty of 50% is applied)

### [Line of fire]()

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

### [Chance to hit target simulation]()

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

### [Chance to hit target execution]()

- if unit pass to hit check then bullet goes directly to target tile
- if unit fail to hit check then new target tile is calculated
  - calculate R = distance to target / max weapon range
  - find new target tile which is in R tiles from original
  - if its the same as target, repeat
- from source to target tile draw a line 
- and check each tile for actual hit, checking its block chance (e.g. fence has 30%, air has 0%, wall has 100%)
- if it hits tile, then execute damage method


### [Movement on battlefield]()

- normal tile cost 1 point to move
- typical human soldier will move between 6-12 tiles per turn when walking
- diagonals tile cost x 1.5 
- no cost to rotate unit in direction
- some terrains cost more to move e.g. sand
- running will cause half speed cost (range is 12-24 tiles) but at cost of always trigger reaction fire 
- crouch move will cost double but will not trigger reaction fire
- stationary position (kneel) cost 1 to start and end 
- using items DO NOT cost speed points

### [Wounds on battlefield]()

- there is no concept of bleeding if you got hit you got wounds
- instead for every high damage hit you get a chance to get a "wound"
  - below 25% of base health = nothing of wound
  - 25-50% of base health = 25% chance of wound
  - 50%-75% of base health = 50% chance of wound
  - 75%-100% of base health = 75% chance of wound
- of course if you hit for max damage unit dies :) 
- stun damage does not count here, its only hurt damage
- wounds are permanent and may cause unit to be crippled (check classes section)
- unit can be healed via medikit during battle to MAX but still will get wound
- it is assumed that wounds cannot be healed during battle, only after (thou health can be to max)
- wound can be losing an eye, broken arm, lose leg etc...

concept behind it:
- health is ability to fight, not exactly your health. If you have 2 of 12 you still can, thou limited to fight
- wounds is your "experience" from battlefield and should be permanent

### [Damage vs Stun]()

- During damage to unit based on weapon damage type we check how much of damage will STUN or HURT unit
- typically for kinetic is 80 to 20 (hurt to stun) but for other damage it could be different
- for every point of damage check is done, its not fixed split

### [Post battle report]()

- earn experience for units
- convert all units into items / research
- collect all objects on ground
- calculate wounds on units
- pay for ammo for all items
- pay for salary for all soldiers (salary or repairs)
- total score for XCOM
- report medals and wounds
- convert all loot into money

### [Reaction fire]()

- turn on overwatch for your soldier by spending 1 AP
- remaing AP will be used for reaction fire
- if enemy unit will be in sight of your soldier then perform reaction stat test and if pass then fire a shot

### [Morale and panic]()

### [Smoke and fire]()

### [Fire mode (snap / auto / aim)]()

- in general there is no concept of fire mode, each weapon has its own fire mode
- unit can enable cover (kneel) to get some stability bonus to accuracy
- unit can enter high land to get some range / visibility bonus
- each weapon has its own AP cost (1-4) and accuracy, range damage, and number of shots per action
- also unit in overwatch will have a chance to fire at enemy unit