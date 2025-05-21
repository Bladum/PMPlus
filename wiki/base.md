
# [Basescape]()

## 

### [Base]()

- typical base is size 5x5 of facilities, which is smaller then XCOM
- there is no limit of bases on world, and in general there might be more bases in general
- in general there are no big facilities
- corridors are very cheap so its easier to construct complex base

### [Gym & Hospital & Psi Lab]()

Gym:
- soldier gets 1 EXP per day
- soldier gets additional 1-3 EXP per day when trained in GYM but up to max of level 2
- advanced gym can train soldiers to level max 3
- advanced gym can allow soldiers to be promoted to more skills via promotion

Hospital:
- wounds are healed based on what wounds definition e.g. 90 days
- health of soldier is healed to max with speed 1 per day
- typical soldier has 6-12 health, which means 12 - 24 days to heal, not taking wounds 
- hospital double the speed of healing HEALTH and WOUNDS
  - without it could be 0.25 per day and with sickbay it could be +0.75 per day so total 1 per day
- some wounds may be permanent and cannot be healed
- some wounds may require special type of hospital (e.g. cybernetic hospital)

Psi Lab and magic:
- there is no concept of PSI training to get skills
- psi lab can add some experience to soldiers under level OR with specific class OR race
- but in general PSI LAB is to allow soldier to unlock new PROMOTION or TRANSFORMATION that will take like 20-40 days (psionic)
- then each class may allow to use specific set of items like spells (facility church) or psi amp (psi lab)

### [Base defence dogfight = base fight]()

- ufo is trying to approach base or bombard it
- some facilities has craft items inside and used as weapons during base defense 
- up to 4 can be used at the same time (4AP limit)
- each facility has HP (base is 10) that defines how damage it can take before destroyed
- damaged facility (above 50% of its HP) will cause to damage content inside (kill people, remove storage etc)
- ufo may have script not to bombard base, BUT to land and attack it
- damage to facilities during this phase will be reflected in base defense mission
  - 100% HP -> nothing
  - 75% HP -> one small explosion
  - 50% HP -> two small explosions
  - 25% HP -> three small explosions
  - 0% HP -> facility is destroyed and removed from base

### [Base defense battle map]()

- build map based on facilities inside
- add some neutral units in some facilities
- add xcom soldiers
- add aliens to facilities marked as OPEN 
- if any facility is damaged during basefight then add some explosions


### [Base defences]()

Same way works base defenses, it is considered to be a craft weapon mounted on base, but more powerful

| Weapon           | Rate | AP | Range | Damage | Chance | Ammo | 
|------------------|------|----|-------|--------|--------|------|
| CANNON DEFENSES  | 8    | 1  | 10    | 1      | 20%    | 200  |
| MISSILE DEFENSES | 3    | 2  | 60    | 15     | 20%    | 200  |
| LASER DEFENSES   | 3    | 1  | 30    | 3      | 20%    | 200  |
| PLASMA DEFENSES  | 2    | 2  | 50    | 7      | 20%    | 200  |
| FUSION DEFENSES  | 1    | 2  | 80    | 30     | 20%    | 200  |

There might be special craft / base weapons that impact ufo on geoscape
- make it slower ?
- make it stop ?
- make it crash ?
- 

### [Base defences dogfight]()

- in general this is same battle like dogfight
- base is a craft with HP depends on number of facilities (each facility has its own health, base is 10)
- all base defenses facilities has craft items inside and used as weapons
- could be more than 4, but only 4 can be used at the same time (4AP limit)
- damage done to base is done to health of each facility, and some of them might be destroyed
- damaged facility could impact content in side like items, soldiers, crafts, research

### [Facilities]()

- idea is similar to xcom, you build structure inside of base
- need to wait N days, spent X money and maybe some resources
- every facility may provide a service which is then required by other facilities / research / manufacturing / soldiers
- base structure is used to generate base defense mission 
- facilities must be connected to each other, but its simple to build corridor between them
- basic image for facility is 32x32 pixels

Base contains some neutral units 
  - towers in corridors
  - engineers in workshop
  - scientists in laboratory
  - technicians in hangar
  - doctors in hospital
  - and everything else is your soldiers

Facilities may improve
  - soldier training
  - soldier healing
  - soldier sanity
  - soldier psi training

Facilities may hold space for
  - soldiers
  - crafts
  - items
  - prisoners
  - live alien

### [Living quarters vs Barracks]()

- game does not have scientists or engineers as people, facilities just generate capacity
- so living quarters is just a barracks for soldiers, assuming to perform some basic training
- more advanced training is done in gym
- more advanced training promotion transformation is done in other places

### [Prisoner]()

- in general non alien live captures are here

### [Live alien]()

- in general alien live captures are here

### [Storage]()

- in general this is just a storage for items

### [Purchasing]()

- on market screen you can order
  - units         kept in barracks / living quarters
  - items         kept in storage
  - crafts        kept in hangar / garage
  - craft items   kept in storage