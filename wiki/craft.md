
# [Interception]() 

### [Crafts movement]()

- craft have speed and range and fuel type
- speed is number of tiles per turn (1 day), which is assumed its 8 hours for calculations
- range is total number of tiles that can be moved BEFORE it crashes

| Craft        | Weapon | Units | Health | Speed | Range | 
|--------------|--------|-------|--------|-------|-------|
| CAR          | 0      | 2/0   | 10     | 8     | 80    |
| VAR          | 0      | 4/0   | 15     | 6     | 80    |
| HELICOPTER   | 0      | 6/0   | 20     | 10    | 24    |
| SKYRANGER    | 0      | 14/2  | 100    | 12    | 32    |
| INTERCEPTION | 2/0    | 2/0   | 150    | 20    | 20    |
| LIGHTING     | 0/1    | 10/0  | 300    | 25    | 60    |
| FIRESTORM    | 0/2    | 1/0   | 400    | 30    | 40    |

Fuel type:
- nothing defined, paid for consumption every mission after return to base
- fuel type is defined by item, and is consumed on every return to base

Ammo type: 
- There is no ammo for crafts, it has just limited number of shots
- it must be re-arm at base 

### [Craft weapons]()

- each craft have capacity for units
  - total number of small units
  - total number of large units
- each craft have capacity for craft items
  - number of small items
  - number of large items (small item will fit into large slot)
- this system gives flexibility what can be mounted into craft
- large unit does not have to be TANK, it could be live unit but it is large, 
- small unit can be mechanical
- this system is same as for units (primary secondary items)

Small items:
- Stingray missile
- laser cannon
- craft cannons

Large items:
- Avalanche missile
- plasma cannon
- fusion balls

Typical craft weapons:

| Weapon        | Rate | AP | Range | Damage | Chance | Ammo   | 
|---------------|------|----|-------|--------|--------|--------|
| CANNON        | 8    | 1  | 10    | 1      | 20%    | 100    |
| HEAVY CANNON  | 6    | 1  | 20    | 2      | 50%    | 50     |
| SMALL MISSILE | 2    | 2  | 40    | 6      | 60%    | 6      |
| LARGE MISSILE | 1    | 3  | 70    | 20     | 40%    | 3      |
| LASER GUN     | 3    | 2  | 30    | 3      | 80%    | 50     |
| PLASMA GUN    | 2    | 2  | 50    | 7      | 50%    | 25     |
| RAILGUN       | 5    | 2  | 30    | 2      | 60%    | 50     |
| BLASTER BOMB  | 1    | 3  | 80    | 30     | 90%    | 3      |


### [Ufo detection]()

- each ufo has a cover power, which means its like health
- it starts with a value of N and every turn xcom crafts and bases which are IN RANGE will reduce it
- if it reaches 0, then ufo is detected and it will be visible on world map
- if ufo will be detected, but will move out of radar range then it disappear again

| Detection buildings | Range | Power |
|---------------------|-------|-------|
| SHORT RADAR         | 5     | 30    |
| LONG RADAR          | 7     | 20    |
| WAVE SCANNER        | 6     | 100   |
| HQ                  | 80    | 1     |
| V HQ                | 80    | 2     |
| CAR                 | 1     | 5     |
| INTERCEPTOR         | 3     | 20    |
| SPY PLANE           | 8     | 50    |

Example:
- global coverage with power 2 but range 300 (global coverage)
- global mission with cover 2 will be detected automatically around world after a day

Example:
- small scout has cover of 50 and cover recovery of 10
- xcom base with short range radar has range of 7 and radar power of 20, will detect UFO after 3 days if in range

Example: 
- any ufo with cover 0 will be detected automatically regardless of range

### [Ufo status]()

- ufo is specific type of location, that can move
- it may move, patrol, land, crash or be static action
- when intercepted there is a mini game
- both bases have defenses that may be used to intercept ufos and xcom craft

Statuses
- patrol    - in air but not moving
- flying    - in air but moving
- landed    - on ground, but not crashed
- crashed   - on ground, but crashed
- defenses  - on ground,
- passive   - static, on ground
- base      - static, on ground, special map

### [Dogfight]()

- when ufo is detected, it will be attacked by xcom craft
- there is mini game based on XCOM dogefight

- there are two sides
  - bottom there is xcoms 
  - top there is ufos 
- distance between them is 100 km
- player for each craft decide what to do this turn
- each craft has 4 AP 
   - move towards enemy 1AP
   - move backwards enemy 1AP
   - speed is number of km is acceleration of craft
   - use weapon or other item (depends on weapon)
- if distance is longer then 100km for 3 turns then battle over

Craft acceleration:
 - very slow aka car / van    2
 - slow aka helicopter        3
 - medium aka skyranger       4
 - medium interceptor         6
 - very fast aka fireceptor   10

This means that 4 AP per turn to move 12km with accel 3



### [Ufo crash]()

- when ufo gets damage above 50% of its health there is a chance to crash, which is based on damage above 50% 
- when it crash on land -> change status and convert to site
- when it crash on water -> remove it (unless its a water ufo)

### [XCOM Craft crash]()

- when xcom craft gets damage it got crash and rescue mission could be done
- this will not save the craft , but may save pilot and items on the craft
- if it crashes over water then its lost

### [Craft Pilots]()

- In general i don't like idea of using soldiers as pilots
- it is better to hire crew like 
- crew can get experience over time and may provide some bonus
- this may be considered as special item loaded into craft
- impact of crew on dogefight
  - low skilled 3AP
  - normal skilled 4AP
  - high skilled 5AP
  - ultra high skilled 6AP