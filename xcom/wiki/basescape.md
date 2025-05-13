
# [Basescape]()

### [Gym & Hospital & Psi Lab]()

Gym:
- soldier gets 1 EXP per day
- soldier gets additional 1-3 EXP per day when trained in GYM but up to max of level 2
- advanced gym can train soldiers to level max 3

Hospital:
- wounds are healed based on what wounds definition e.g. 90 days
- health of soldier is healed to max with speed 0.5 per day
- typical soldier has 6-12 health, which means 12 - 24 days to heal, not taking wounds 
- hospital double the speed of healing HEALTH and WOUNDS
- some wounds may be permanent and cannot be healed
- some wounds may require special type of hospital (e.g. cybernetic hospital)

Psi Lab and magic:
- there is no concept of PSI training to get skills
- psi lab can add some experience to soldiers under level OR with specific class OR race
- but in general PSI LAB is to allow soldier to unlock new PROMOTION or TRANSFORMATION that will take like 20-40 days (psionic)
- then each class may allow to use specific set of items like spells (facility church) or psi amp (psi lab)

### [Base defence dogfight = basefight]()

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

### [Base defense]()

- build map based on facilities inside
- add some neutral units in some facilities
- add xcom soldiers
- add aliens to facilities marked as OPEN 
- if any facility is damaged during basefight then add some explosions

### [Normal market]()

- in general some item can be bought and all items can be sold
- each item supposed to have supplier
- supplier diplomacy status impact price and availability
  - you cannot purchase from enemies
  - prices from allies are lower by 25%
  - prices from neutral are normal

### [Black market ]()

- ??

### [Manufacturing]()

- this is done in very similar way like in XCOM
- main difference there is no engineers concept, instead each facility has its own production capacity
- workshop gives capacity for 25 Man Days and this will be total TIME used on project
- manufacturing only cost for salary if something is being build, e.g. time to build
- cost of items (both time, resources, money) are fixed

### [Research]() 

- This is done very similar way like in XCOM
- main difference is that there is no concept of scientists, instead each facility has its own research capacity
- laboratory gives capacity for 25 Man Days and this will be total TIME used on project
- research only cost for salary if something is being researched, e.g. time to research
- cost of research is random for all research and setup when game starts at aprox 50-150% of baseline
- research is streamlined, if something cost 50MD and random value would be 54MD, then game will display progress in %
- there are no other hidden mechanism like chance to discover or number of scientists etc...

Things which are done differently:
- in general, you dont need to create item from battlefield to allow to research it
- if there are items only for this (aka story) then we will directly unlock research for player
- so there is no need to create items only for story purpose

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