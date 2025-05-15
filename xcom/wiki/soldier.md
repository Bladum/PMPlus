
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

- reaction            5 -> 12   dodge during mean, reaction in enemy move
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

### [Skill]()

- skill is addon to unit that boost stats in specific way
- skill is generic mechanism used in many different ways:
  - as **promotion** of soldier for experience
  - as special skill for soldier to simulate their **background career** before XCOM
  - as way to build enemy units from **classes**
  - as way to **transform** soldiers other than promotion via experience (e.g. cyborg)
  - as way to simulate permanent **wounds** from battles e.g. lost leg
  - as way to simulate **temporary effects** during battle e.g. bloodlust
  - as way to simulate special awards on battlefields aka **medals**
  - as way to simulate **perks**, which are manually selected additional skill, very narrow

#### [Promotion]() 

- Soldier once get enough experience he can collect new skill
- Same skill can be acquired multiply times
- Each skill gives some permanent bonus to stats ( e.g. sniper +2 aim)
- Some skill may be acquired only once or few times
- Some skill may be required for items

skill for xcom:
- scout
- soldier
- sniper
- medic
- heavy
- assault
- ninja
- commander
- psychic
- engineer
- pilot

#### [Transformations]()

- transformation is very similar to promotion but it's not used when level up
- transformation are expensive, long term changes to unit stats
- they usually require resources, money, time and facility in base

#### [Classes]()

- Same mechanism is used to build unit templates for battles
- typical enemy unit is build from: 
  - race
  - level, that defines set of skill e.g. soldier + soldier + engineer
  - armour, primary weapon, secondary weapons
- other than that it works for enemy same way like promotion for x-com

#### [Background Careers]()

- Each xcom soldier might have a special one time skill 
- this represents background of soldier 
- careers are only used during creation of unit, they cannot be acquired by promotion

#### [Auras]()

- aura is temporary skill assigned to soldier to simulate special effect like bleeding, bloodlust, panic etc
- auras are removed from solder after battle ends

#### [Medals]()

- soldier may acquire medal for completing special mission 
- medal is one time skill and cannot be got another way
- it may boost stats in special way

#### [Wounds]()

- soldier if hit may get a wound 
- there is no concept of bleeding in game
- after battle each would, may cause a permanent would that would cripple the soldier e.g. lost leg
- woulds may or may not be treatable or very long time

#### [Perks]()

- special ability that is assigned to soldier
- usually it should add one major advantage and one disadvantage
- perks are not permanent, they can be removed, but only one can be assigned to soldier at any time
- perks required special level of unit
- this is similar to perks in Fallout game 
- soldier may need to spent some time to activate perk

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
- due to race some units may get experience or not, which means they could get skills by promotion
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