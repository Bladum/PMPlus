
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
- multiply faction may have single race (each cult faction has race as human, but with some special ranks)
- factions cannot be removed but their campaigns can be activated / deactivated either by research or by calendar

### [Factions]()

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

- is physical place on world map
- it may be xcom base, alien base, xcom craft, alien ufo, city, site

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


