
# [Lore & Campaign]()

### [Calendar]()

- geo game is turn based, 1 day = 1 turn, 30 days = 1 month
- at start of each month campaigns are created (check below)
- at specific moment in game e.g. some more campaigns are created e.g. alien invasion via calendar
- entire concept behind calendar is that every month more and more campaigns are created until end game (tower defense)
- player can block some campaigns by completing some research but also they are triggered due to calendar (min max month)
- campaign does not trigger auto-scaling of difficult of alien units inventory like in XCOM

### [Story design mechanics]()

- Factions are designed for arcs, so in general one arc is one faction
- Factions story should be more or less independent of each other, usually they do provide some benefits
- campaigns are per faction, so each faction has its own campaign
- single faction may have multiple races (alien faction has race sectoid, floater etc)
- multiply faction may have single race (each cult faction has race as human, but with some special classes)
- factions cannot be removed but their campaigns can be activated / deactivated either by research or by calendar

### [Factions = Organizations]()

- factions defined who is who on mission / craft / base level
- faction can be either allied, neutral or enemy to xcom
- if they score points and are enemy player will lose score, if they are allied player will gain score
- on some worlds like mars there might be only one faction
- faction may have a missions, that creates ufos, create base, create site
- so in general faction always owns locations on map

### [Missions]()

- Every month game generate random campaign of specific faction based on data in calendar
- each campaign must met some requirements e.g. calendar, research etc
- each campaign has a faction and goal / type
- each mission will trigger creation of missions in waves
- each campaign will be created within regions with weights
- when campaign is completed faction will score points and depends on diplomacy xcom will lose or gain points
- missions from single campaign can overlap to next months causing massive chaos in short time
- missions are created in waves, so each wave has its own delay and may overlap sometimes

### [Locations]()

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

### [Enemy score points when...]()

- entire mission is completed
- for ufo that was not destroyed on time
- if single wave completed its task
- for everyday when alien base exist
- some ufo trajectories may have special score for each turn

### [Events]()

- events is a separate mechanism from missions
- events are on single list, may have some calendar or research prerequisites
- events have chance / weights to be triggered
- at start of each month random number of events are generated to happen during this month
- events may have max number of occurrences within a game, within a month, within a year
- calendar does not control events, its just random number each month

Events examples:

- change player money
- change player items
- change player score
- change player research
- change player unit 
- change player facility in base
- create ufo in specific region with specific trajectory

### [Quest]()

- is a simple list of flags that could be used to track some events
- quest can be used as prerequisite in many place just like research
- it is advised to use this flag system instead of adding research
- its optional, research can be used
- game progress is calculated based on number of quests completed


