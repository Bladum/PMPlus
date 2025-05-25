
# [Soldiers]() 


### [Recruitment]()

- in general purchasing and manufacturing projects can deliver unit
- unit must have a race, and race in general may have fixed stats
- but when unlocking new technology new race can be unlocked with better / other stats
- new race will have different options for classes / item usage

### [Race]()

- Soldier basic information is race, e.g. human, sectoid, wolf, zombie
- race defines basic stats (could be fixed or random) and stat max 
- race may define some items usage or classes usage
- race defines how unit looks like (sprite) on battlefield

### [Unit stats]()

- speed               6 -> 12   movement speed per AP
- strength            6 -> 12   bonus to HTH, range of throw, capacity
- health              6 -> 12   life
- energy              6 -> 12   stamina, for items, run and magic

- reaction            5 -> 12   dodge during melee, reaction in enemy move
- melee               5 -> 12   HTH
- aim                 5 -> 12   accuracy for firing and throwing
- sanity              5 -> 12   sanity, only for xcom

- psi                 1 -> 12   psionic / magic skill
- will                3 -> 12   bravery
- morale              max 10    during battle only

- sight               20 / 10   distance of sight for day / night in one direction
- sense               field of view in all directions
- stealth             how impact other units detection  

- size                small / large (1 or 4 tiles)


### [Soldier inventory]()

- game does not have inventory other than
  - armour, cannot be changed during battle
  - primary weapon, has ammo in build, no separate clip
  - 2 x secondary weapons, has ammo in build, no separate clip
  - due to some specific armours, unit might have different combination of weapons / equipment but total 4

### [Soldier faces]()

- White, Black, Asian 
- Female vs Male
- 8 per combination
- soldier has gender male or female (maybe be a class to simulate it)
- soldier may be one from 8 faces for male / female but only as visual representation, not on battle its too small

### [Unit size]()

- all units on battlefield are units, thou they might be small (1x1) or large (2x2)
- large units are usually vehicles or large aliens but its not a rule
- large units are equipped same way like small one, thou usually its different race
- due to race some units may get experience or not, which means they could get traits by promotion
- a tank, large mechanical unit, may not get experience via battle, but may have transformation like new armour type
- unit may have predefined items like armour or weapon, and cannot be changed
- crafts have cargo space for small and large unit separately

### [Experience]()

Ways to get experience:
- +1 day in base
- +2 day in base with training facility
- 1 mission = +10 EXP
- hits (1 HP lost = 1 EXP)
- wounds (1 wound = 10 EXP)
- kills or stuns (EXP gained = score value of this unit)

Faster experience ?
- intelligence of soldier may impact how fast he gets experience

#### [Levels of experience levels]()

| Level  | Experience |
|--------|------------|
| 0      | 0          |
| 1      | 100        |
| 2      | 300        |
| 3      | 600        |
| 4      | 1000       |
| 5      | 1500       |
| 6      | 2100       |