
# [Lore & Campaign]()

### [Campaign]()

- geo game is turn based, 1 day = 1 turn, 30 days = 1 month
- at start of each month missions are created (check below)
- at specific moment in game e.g. some more missions are created e.g. alien invasion via calendar
- entire concept behind campaign is that every month more and more missions are created until end game (tower defense)
- player can block some mission by completing some research but also they are triggered due to calendar (min max month)
- campaign does not trigger auto-scaling of difficult of alien units inventory like in XCOM

### [Story design mechanics]()

- Factions are designed for arcs, so in general one arc is one faction
- Factions story should be more or less independent of each other, usually they do provide some benefits
- missions are per faction, so each faction has its own missions
- single faction may have multiple races (alien faction has race sectoid, floater etc)
- multiply faction may have single race (each cult faction has race as human, but with some special classes)
- factions cannot be removed but their missions can be activated / deactivated either by research or by calendar

### [Factions = Organizations]()

- factions defined who is who on mission / craft / base level
- faction can be either allied, neutral or enemy to xcom
- if they score points and are enemy player will lose score, if they are allied player will gain score
- on some worlds like mars there might be only one faction
- faction may have a missions, that creates ufos, create base
- so in general faction always owns something on map

### [Missions]()

- Every month game generate random mission of specific faction based on data in calendar
- each mission must met some requirements e.g. calendar, research etc
- each mission has a faction and goal / type
- each mission will trigger creation of ufos in waves
- each mission will be created within regions with weights
- when mission is completed faction will score points and depends on diplomacy xcom will lose or gain points
- waves from single mission can overlap to next months causing massive chaos in short time

### [Ufos (on world map)]()

- ufo is created by mission, single wave may have multiple ufos, single wave takes n day before next wave
- it is always created as ufo, even when its a static battle in jungle with monsters
- so technically speaking everything which is NOT CITY or XCOM is a UFO

### [Ufo wave]()

- Every mission has a wave of ufos, which also could be just one
- each wave has a delay between each other, but single wave could be 3 ufos
- ufo are places in same region like entire mission
- ufo has assigned ufo trajectory that defined what to do with this ufo
- after N days / turns next way is created until all waves are send

### [Ufo trajectory]()

- ufo can travel according to some steps e.g.
- start with region, go to city, land, wait N turns, go to another city, land, wait N turns, go to another region
- this is scripted and defines how ufo moves around the world map
- if step cannot be performed then its is skipped
- ufo trajectory is not linked with specific ufo, rather its a template of movement and assigned on mission level
- basic mission for cults is just to spawn passive ufo for N days so player can react to it

### [Ufo score when...]()

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

### [Calendar]()

- basic mechanism to trigger events, missions or ufos
- just check specific date and trigger it