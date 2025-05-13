
# [Soldiers]() 

### [Race and face]()

- soldier has gender male or female (maybe be a class to simulate it)
- soldier may be one from 8 faces for male / female but only as visual representation, not on battle its too small

### [Nationality]()

- Soldier can be from any country that funds XCOM

### [Recruitment]()

- soldier must have a race, and race in general may have fixed stats
- but when unlocking new technology new race can be unlocked with better / other stats
- new race will have different options for classes / item usage
- another option is to buy a standard race (human) but on level higher (1-2-3) so player can select classes to promote him

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
- size                small / large (1 or 4 tiles)
- stealth             how impact other units detection  

### [Class]()

- class is addon to unit that boost stats in specific way
- class is generic mechanism used in many different ways:
  - as **promotion** of soldier for experience
  - as special class for soldier to simulate their **background career** before XCOM
  - as way to build enemy units from **templates**
  - as way to **transform** soldiers other than promotion via experience (e.g. cyborg)
  - as way to simulate permanent **wounds** from battles e.g. lost leg
  - as way to simulate **temporary effects** during battle e.g. bloodlust
  - as way to simulate special awards on battlefields aka **medals**

### [Promotion]() 

- Soldier once get enough experience he can collect new class
- Same class can be acquired multiply times
- Each class gives some permanent bonus to stats ( e.g. sniper +2 aim)
- Some classes may be acquired only once or few times
- Some classes may be required for items

Example: 
- Tom, soldier xcom, race human, level 3
- classes: sniper, sniper, scout

Ways to get experience:
- 1 day in base
- 1 day in base with training facility
- 1 mission
- kills & wounds

Soldier experience levels to get promotion:
- 0 
- 100
- 300
- 600
- 1000
- 1500
- 2100

Classes for xcom:
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

### [Transformations]()

- transformation is very similar to promotion but it's not used when level up
- transformation are expensive, long term changes to unit stats
- they usually require resources, money, time and facility in base

### [Enemy unit templates]()

- Same mechanism is used to build unit templates for battles
- typical enemy unit is build from: 
 - race
 - level, that defines set of classes e.g. soldier + soldier + engineer
 - armour, primary weapon, secondary weapon
- other than that it works for enemy same way like promotion for x-com

### [Background Careers]()

- Each xcom soldier might have a special one time class 
- this represents background of soldier 
- careers are only used here, they cannot be acquired by promotion

### [Auras]()

- aura is temporary class assigned to soldier to simulate special effect like bleeding, bloodlust, panic etc
- auras are removed from solder after battle ends

### [Medals]()

- soldier may acquire medal for completing special mission 
- medal is one time class and cannot be got another way
- it may boost stats in special way

### [Wounds]()

- soldier if hit may get a wound 
- there is no concept of bleeding in game
- after battle each would, may cause a permanent would that would cripple the soldier e.g. lost leg
- woulds may or may not be treatable or very long time

### [Soldier inventory screen]()

- game does not have inventory other then
  - armour, cannot be changed during battle
  - primary weapon, has ammo
  - 2 x secondary weapons, has ammo

### [Sanity]() 

- damage to sanity is applied only at the end of mission, not during
  - low mission -1
  - med mission -2
  - high mission -3
- sanity is recovered normally 1 per week
- some facilities may improve this rate
- this may be linked to race (sanity recovery)
- sanity does not change during battle, its only for geo game

Sanity impact:
- >= 10 -> +1 AP
- <= 3 -> -1 AP
- <= 2 -> -2 AP
- <= 1 -> -3 AP
- <= 0 -> -4 AP

### [Morale]()

- under stress unit will perform a WILL test 
- if unit fail then it will lose 1 morale
- morale is recovered after battle to max
- morale is recovered normally 1 per turn if REST is used
- some actions may cause several morale tests

Morale impact is same as sanity but for this battle only:
- >= 10 -> +1 AP
- <= 3 -> -1 AP
- <= 2 -> -2 AP
- <= 1 -> -3 AP
- <= 0 -> -4 AP

### [Soldier faces]()

- White, Black, Asian, 
- Female vs Male
- 8 per combination

### [Action points / Time Units]()

- each unit has speed from 6 to 12 for human, typically 8, this defines only movement
- movement cost 2 point on normal tile, more on hard tile
- movement cost 3 when moving diagonally (always 50% more)
- rotation cost is 1 per 90 degrees

each unit has 4 AP which can be used for:
  - move
  - reload
  - cover (aka crouch / kneel)
  - overwatch (aka reaction fire)
  - use item (shoot, throw, use)
  - rest
  - throw item (primary / secondary)

What can impact action points ?
  - in general its all 4 AP
  - some auras like BERZERK may increase AP +1
  - some auras like PANIC may decrease AP -1

Use cost:
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

Overwatch action:
  - move unit into watching mode, it will use remaining AP to fire at enemy

Cover action:
  - move unit into cover mode, it will focus on better AIM and become smaller target

Rest action: 
  - spent AP to recover energy / morale

Move action: 
  - spent AP to move unit, move range is based on unit speed
  - typical unit with speed 8 can move 4 tiles per 1 AP, and 16 tiles per turn for all AP

Stealth move action:
  - spent 2 AP to move unit just like move action but WILL NOT trigger reaction fire from enemy

Suppress action:
  - try to aim at enemy but do not fire, it will something limit enemy AP next turn