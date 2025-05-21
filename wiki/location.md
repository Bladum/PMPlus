
## [Locations]()

- missions are created by campaign and will create location in specific tile of world 
  - it could be flying and moving UFO
  - it could be static site
  - it could be permanent alien base
- several locations could be created at once within single day of a mission
- each type of location has its own logic to be processed later

#### [Ufo]()

- ufo is moving location
- it has a ufo script that mange how its being moved
- if its path is done then it disappears
- must be first intercepted by craft, unless it lands / crashes
- if it crashes then it becomes a site
- ufo via its ufo script can spawn more sites or an alien base

#### [Site]()

- sites are static locations
- they do wait until picked by xcom
- when they disappear xcom lose score

#### [Alien base]()

- alien base is static location
- it was its own mechanism after creation how to growth in size and expand
- it has max 3 levels and can sent more missions in time

### [Mechanism for alien base]()

- alien base is created its always level 1
- every month it will sent missions
  - research mission in the same region to find cities and xcom bases
  - supply mission to it self from another region and if not intercepted it will grow 1 level
  - hunt missions to attack xcom crafts in region 
  - infiltration mission to corrupt country
  - retaliation mission to attack xcom base
  - alien base mission to create new base 
- each level of base cost xcom 5 points per day, so level 4 cost 20 points per ay, 600 points per month
- number of type of missions will depend on level of base
- level of base will impact what is size of base during battle
- alien base mission are always 2 levels
  - on ground to get to the entrance
  - underground to get to the core
- level of base will define number of soldiers and map size
  - 1 is 4x4 and 20 units per level
  - 2 is 5x5 and 30 units per level
  - 3 is 6x6 and 40 units per level
  - 4 is 7x7 and 50 units per level
- level of base defines number of random missions it creates, 1 level = 1 mission per month
 
#### [Ufo script]()

- ufo can travel according to some steps e.g.
- start with region, go to city, land, wait N turns, go to another city, land, wait N turns, go to another region
- this is scripted and defines how ufo moves around the world map
- if step cannot be performed then its is skipped
- ufo trajectory is not linked with specific ufo, rather its a template of movement and assigned on mission level
- basic mission for cults is just to spawn passive ufo for N days so player can react to it
