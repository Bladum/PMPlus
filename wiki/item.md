

# [Items]()

### [Item types]()

- items used by crafts as weapons
- items used by units
    - primary item aka weapons
    - secondary items aka equipment
    - armours
- live captured units, that must be kept in prisons
- special resources, that must be kept in special container

### [Unit Items]()

Armours:
- light
- arm vest
- personal armour
- power armour

Primary weapons: 
- rifle
- sword
- SMG
- shotgun
- sniper rifle
- rocket launcher
- heavy cannon
- machine gun

Secondary weapons:
- grenade
- pistol
- knife
- medikit
- flare
- motion scanner
- psi amp
- stun rod


### [Ammunition]()

- primary / secondary weapons does have limited ammo but only for this battle
- there is no item in game to represent ammo, it is part of weapon
- some weapons may have very large capacity e.g. 999
- some weapons may regenerate ammo during battle e.g. lasers
- some weapons may have small capacity e.g. 2 but they are free to replenish after
- to simulate improved ammo for xcom weapons, just create new type of weapon with different stats
- after battle ammo is replenished to max value for free
- cost of ammo is included in weapon cost, so you do not need to pay for it


### [Ammo clips]()

- in general there is no ammo clips like xcom 
- weapons have ammo capacity, that is used during battle and that is 
- its replenished after battle and player must pay for it 
- this may give interesting meachincs e.g.
  - use alien heavy plasma with 20 shots but very expensive to replenish
  - or convert weapon to human plasma with 30 shots but cheaper to replenish
- game has special type of ammo called ammo box that provide generic way to replenish ammo during battle
  - all laser weapons can be replenished with "laser battery" ammo box
  - all conventional light weapon can be replenished with "ammo" ammo box
  - all heavy weapons can be replenished with "heavy ammo" ammo box
  - alien weapon cannot be replenished, but can be converted to human weapon with
  - rocket launcher can be replenished with "rockets" ammo box
- usually ammo box is heavy
- it replenishes weapon to its full capacity and is consumed in the process

### [Ammo before battle]()

- before battle inventory screen, player can change which ammo type is used in weapon
- each ammo always cost / weights the same as it just part of weapon, it may have different stats for the period of battle
- once you select type of ammo, you can only use it during this battle, like only AP or HE

Autocannon options: 
- AP, 12 shots, high ap damage
- HE, 10 shots, high explosive damage

### [1 or 2 handed weapons ?]()

- game assumes that soldier handles in which hand he is using weapons
- that is why some items are primary or secondary 
- there is no cost of switching between them, just use primary or secondary
- there is assumption that primary weapon usually is 2-handed and secondary is 1-handed


### [Unit armour]()

- armour objects DO NOT have direction, there is just value e.g. 7
- armour objects DO have armour resistance, that modify power before damage is calculated
- armour is NOT visual representation of unit on battle, actual unit is
- armour can overwrite race sprite for this unit

### [Armour resistance]()

Use both on weapons and armours, to calculate final damage to unit

- kinetic
- explosive
- laser
- plasma
- psionic
- bio
- acid
- stun
- smoke
- fire

Due to small scale of damage, it is better to use larger values e.g. 125% or nothing

### [Weapon range]()

- you can use weapon without limitation within range
- you CANNOT use weapon outside range

### [Example values]()

Items weight:
- grenade 1
- pistol 2
- rifle 4
- medikit 2
- mine 3
- heavy cannon 6
- light armour 1-2
- medium armour 3
- heavy armour 4-6
- minigun 10

Weapon damage: 
- shotgun 3
- SMG 4
- pistol 5
- rifle 6
- sniper rifle 7
- laser pistol 8
- plasma pistol 11
- heavy plasma 22
- rocket 24 / 3 drop
- grenade 12 / 2 drop
- plasma grenade 18 / 3 drop 
- blaster bomb 36 / 4 drop

Range of sight:
- human day 20
- human night 10
- scout class +3

Range of fire:
- shotgun 5
- SMG 10
- pistol 15
- rifle 30
- sniper 45

Armour value:
- light 1
- armoured vest 5
- personal arm 8
- personal + shield 12
- tank 24-28
- power armour 20

Unit stats (HP):
- human rookie  6
- human expert 12-14
- alien sectoid 4
- alien monster 24

Typical ammo size clip:
- pistol 30
- heavy pistol 20
- SMG 150
- rifle 60
- knife 999
- power sword 12
- shotgun 15
- plasma rifle 30
- heavy plasma 20
- blaster bomb 2
- stun bomb 4
- rocket launcher 3
- grenade 2-4
- medikit 5

### [Weapon use modes during battle]()

- weapon may allow to use other modes then SNAP
- they have common modifiers but weapon may or may not allow to use them
- this is defined on global level, not on item level
  - each mode other than SNAP must be defined

| Mode  | Key     | AP Cost | Range | Accuracy | Shots | Damage |
|-------|---------|---------|-------|----------|-------|--------|
| SNAP  | -       | 100%    | 100%  | 100%     | 1     | 100%   |
| AIM   | Control | 175%    | 100%  | 150%     | 1     | 100%   |
| HIGH  | Alt     | 150%    | 100%  | 75%      | 1     | 150%   |
| AUTO  | Shift   | 125%    | 100%  | 50%      | 3     | 100%   |
| FAST  | Alt     | 75%     | 100%  | 75%      | 1     | 100%   |
| FAR   | Alt     | 125%    | 150%  | 75%      | 1     | 75%    | 

- check for AP left is done before applying modifiers
- so unit may have negative AP for the next turn

### [Armours and inventory slots]()

- armours may have slots for primary / secondary items
- standard setup is 1 + 2, but heavy armour might have 1 + 1
- some special armour may have even 2 weapons
- total number of primary + secondary items max is 4

Example
- suit 1 + 1
- suit with bag 1 + 3
- vest 1 + 2
- vest and shield 1 + 1

### [Manufacturing and purchasing project for items]()

- all items can be sold
- some items can be bought on market
- some items can be manufactured
- all is configurable in proper sections
- units / items / crafts are 3 categories that can be managed here