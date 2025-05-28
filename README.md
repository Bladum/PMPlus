
# Welcome to AlienFall

AlienFall is strategic game with tactical layer and some sandbox / simulation elements. 
It covers rise and fall of Covert organization managed by player.
It starts as startup and ends as multiplanetary full scale military organization. 
It is open-ended, it does not have to be war against aliens. 

Discord https://discord.gg/7wGAUDUd

![banner](https://github.com/user-attachments/assets/c604e0ce-8e6d-42a4-89c4-6aca1c16a2fa)

# TL;DR

- AlienFall is a turn based strategy game with
  - strategic layer with geoscape and missions
  - battle scape with tactical combat
  - base management to prepare for next missions
  - research tree to unlock new options
  - open-ended with no fixed lose or win conditions
  - some sandbox and simulation elements 

# Core design principles and assumption 

- It's not a OXC clone. 
- Made for fun and to have practical working experience with AI Agentic Codding.
- Open source, non-commercial, free to play. Probably MIT or something.
- Supports rather larger mods (total conversion) than many smaller ones (or sub-mods).
- Documentation in wiki is mainly for AI Agent in human-readable format, so it can be used to generate mods and engine and integrate them. 

## Game mechanics design principles

- In general game have set of generic mechanics that should cover most cases, and customization of these mechanics is fine. 
- Adding completely new mechanics is not preferred, unless it is generic and can be used in other cases.
- Reliability over functionality, so it should be easy to use and understand (by AI Agent)
- Balance between details of mechanics in different areas (inventory vs unit development vs LOFT system).
- No external scripting language (at least for now).
- Common use of mechanics for several cases to reduce complexity
  - Traits system for ranks, medals, mutations, origins, effects,  perks, wounds, etc
  - Quests system for research, lore, events, missions, etc
  - Ammo system for items, crafts (like in Arcanum)
  - Salary system for all rearm, repairs, maintenance, research, manufacturing, man hours work

## Use of Generative AI

- for content that is visible to player, could be used but preferable not
- for content that IS NOT visible to player, by design it should be used
- at some point i would allow other users to use AI to generate content (private AI server) for mods, but not now

## User interface design principles

- Graphics and visual effect are not priority, thou UI might be modern. 
- Graphics all is pixel art and symbolic, to be upscaled to 32x32.
- Minimize clutter with UI, lack of nested UI screens. 
- Remove screens that can be automated or simplified or just FYI to player. 
- Minimize number of popups, and apply notification system instead.
- Player is informed about game data if research / lore is completed (e.g. damage done to unit during battle).

## Financial design principles

- There is additional layer in game like FinOps to control costs and income.
- Most costs comes from usage / time & material and are not fixed.
- Every month player gets invoice for all costs, and then funding from countries is just one way to get money.
- There are much more ways to make and spend money in variable ways.
  - Engineers and scientists are paid only when work
  - Reload of weapons after battle instead of making / buying clips
  - Repair / rearm / refuel of crafts after interception
  - Training and recovery of soldiers
  - Sending soldiers to battle is not free, and they are paid per mission
- So sending craft to city and start mission would be like raid. You will get loot but lose score -> funding. 

- XCOM has mostly fixed costs, which was simple to manage and difficult to optimize. 

## Geoscape design principles

- Crafts have units loaded into them, not unit items. 
- Strategic game is turn based, with 1 turn = 1 day. 
- Crafts move on world map similar way like during battle, but with different speed and range.
- Both geo, base and battle scape are turn based, top down views and flat 2D map.
- Craft for player has same data / mechanics  (with craft items), it just have script to simulate different behavior.
- Detection is based on detection range and power, and cover capacity. If cover is zero or less, then mission is detected.
- Game has support for multiple worlds, like Mars or Moon, with different tiles and biomes or sizes. 
- Countries only exists on Earth (for funding purposes), and regions are used for mission generation on all worlds. 

## Basescape design principles

- Bases are smaller (5x5) but with larger number on map. 
- Facilities do provide generic capacity feature for engineering, science, living, storage, prison, recovery, training, etc.
- Crafts are not assigned to hangar, it just take craft space in base. 
- There is no concept of engineers or scientists, instead there is generic capacity for work in base.
- If lab is not working you pay for maintenance of facility, but not for work / salary.

## Battlescape design principles

- Line of sight is used and is more important than level of lighting (like in RTS game with fog of war).
- Units for player has same data / mechanics as for enemy (with armour, items, stats), it just have script to simulate different behavior.
- Night and day cycle is simplified. There is either day or night during battle.
- Units have items loaded into them, with inventory slots: armour | primary weapon | up to 3 secondary weapons.
- Units gain experience but are manually level up (promotion system) with specific stats only to be improved. 
- Items do not have clips per item, rather they have limited ammo per battle with some generic ammo types (like laser batter for all laser weapons).
- Limit micromanagement e.g. in inventory, ammo, etc. Remove mechanics that are not fun to use.

## Lore specific design principles

- There is no assumption that player organization is good or bad like defending Earth from aliens or evil organization.
- There is just assumption that player organization is covert, and it is not known to public at least to some extent.
- Score and funding mechanics is based on player score only, which is one of ways to make money. This like official good way to get money. 
- If you want to play as evil organization, you can do it, but will have to find alternative way to get funding.
- Fully support all lore elements and features from mod X-Com Files, one way or another.
- Player organization is growing in time, both in size and complexity (in build organization upgrade mechanics).
- Lore specific elements have separate mechanics (quests), so research don't have to be used. 
- In general player should feel increase level of difficulty:
  - campaigns generate more and more mission every month, unless research locks them (like in tower defense game)
  - soldiers gain experience and level up only in specific area, so no superheroes at the end of game
  - soldiers gain heavy wounds and traits, that may impact their performance for long time


# FAQ 


### What is AlienFall?

- It's a game with its own in vanilla mod to play it. Made in python (at least for now).
- I would not call it a game engine, just configurable game.
- It is designed for very specific use -> 
- All is done via mods, which are just text files. 

## Why this name or logo ? What it means ?

- Alien in this case means any one who is not us. Alien can be a person from another country or religion. 
- Fall means that we want to survive and make other (aliens) fall.
- So in other words we want to perform covert infiltration, and make other fall, so we can survive. 

Who is doing like this ? 
- Logo is a symbol of tick (kleszcz) :)  
- The tick symbolizes covert infiltration, persistence, and survival—core themes of AlienFall. 
- In Polish culture, the tick is both a symbol of something alien and a metaphor for causing a "fall." 
- The icon reflects the player’s journey: starting small, operating in the shadows, and ultimately bringing down much larger adversaries.
- It does not mean we are good :) it means we want to survive and make others fall (or we will fall)

### Is it clone of XCOM?

- Yes, it is inspired by XCOM, but it is not a clone. 
- It has elements of many other games, if it fun to use and easy to implement by AI Agent.
- There is no assumption that is must be here because it was in XCOM.

### How this is related to OXC mod called X-Com Files ?

- AlienFall should fully support all features required by this mod, one way or another. 
- It does not mean it has to be exactly same like in OXC, but it should be similar experience for player.

### Why make another game like XCOM ?

- It's not about a game itself, but how its build. With agentic codding.  
- 3 main elements:
  - docs = human-readable documentation about game mechanics and everything else in markdown format
  - mods = yaml based configuration files for game configuration aka mod
  - engine = game engine is written in python, to execute both above
  
- Agentic codding:
  - autonomous agentic AI is to manage all 3 elements, to make it integrated and reliable
  - people focus on if game mechanics are fun and free of issues, provide feedback and ideas
  - no resources are included in the loop, It's only about text and code (at least for now)
  - AI Agent can support in all 3 elements, but it is not required, people can do it too

## Why Python ? 

- Python is easy to read and write, and has good support for AI.
- Pyside6 ( Qt ) is great media library for GUI, and it is cross platform, have great documentation and examples.
- Python is not the fastest language, but it is fast enough for this game.
- In case ultra performance is needed, it can be done in module that is in C++ and wrapped in python.
- Python is one of most popular languages for AI, so it is easy to find help and resources.
- Entire game is as code, which is designed to be cocreated with AI Agent. 

### Why its different to make game with AI Agent?

- AI Agent can work on all 3 elements at once and integrate them
- Usually it starts with docs, then mods element and then engine it self (which is reversed for classical approach)
- This allows people to focus on game mechanics and fun, rather than implementation details

### How mods are supported ?

- Mods is set of configuration files in folder like in OXC
- It is more designed for total conversions (bigger larger mod) rather than smaller mini mods

### Who make decision to include or not include?

- It's not a matter if its according to design, but if it works (AI), is doable (dev) and is fun to use (modder).
- Game architecture have some basic generic mechanics, and in most cases new feature would be extension of existing mechanics rather than new one.

## What it means its open-ended game?

- Specific technology or quest or mission may trigger a cinematic event, which will display to player, but it does not end the game.
- Quest mechanics are used to track progress of game, and to trigger events but it does not have end the game. 
- Every game would be different based on types of campaigns generated every month, which means total number of quests might be different per game.

### Why this is strategic game?

- Geoscape and handling missions on world map
- Base and resource management
- Technology research

### Why this is tactical game?

- Interception of enemy crafts is mini tactical game
- Land battlescape with tactical combat on single unit level

### Why this is sandbox game?

- There is no fixed end, no strict win or lose conditions, and player can start missions on empty tiles.

### Why this is simulator game ?

- Battle scape has destructible terrain, neutral units have more complex behavior.
- More RPG elements on units: traits and stats system. 
- Geoscape:

# Difference vs XCOM

## Globe

- game has 2D map that represents Earth, aprox 90x45 tiles
- there might be other worlds with different tiles like Mars or Moon
- single tile has a biome, which is a type of terrain
- single tile must be in region, and may have a country owner
- city takes entire tile
- mission are generated on tiles, there might be single mission on single tile

## Detection on globe

- each xcom base and xcom craft has a detection range and detection power
- each enemy mission have cover power and cover recovery
- every turn every mission in range of radar will lose cover power, and when zero or less its detected
- if mission is detected, it will be visible on world map and action can be performed

## Location types

- there are 3 types of location:
  - alien base - static permanent mission that may grow in time and may generate its own missions nearby
  - site - static mission without major logic, cannot be intercepted, will disappear after some time
  - ufo - moving mission with its own ufo script to simulate different scenarios / actions, can be intercepted

## Timescale

- Geo is turn based, 1 day = 1 turn
- simplified night day cycle, in which 1 full day takes entire month
- each month has 30 days

## Battle 

- terrain has map blocks, that is build from tiles
- map block is flat, there is floor, wall, item, roof on single layer
- floor might have height with slope, but in general its one level
- each map block is 15x15 or multiple of it
- battles are small (4x4 block) medium (5x5 block) and large (6x6 block)
- battles have different objectives, other than kill all enemies

#### Graphics 

- each tile is now 16x16 pixels top down with symbolic graphics, to be upscaled to 32x32

#### Line of sight during battle

- there is no LOFT mechanism during battle
- instead all line of sight, line of fire, detection is done by using partial coverage mechanism
  - block either blocks or does not block, or block partially 
- accuracy is based on distance and cover, and cone of fire is used 
- slope and height of floor might be used to cover and limit sight 

#### Fog of war and lighting

- lighting is used to simulate day and night but also 
- there is only 2 types of natural light: either night or day
- there might be source of light inside elements on tile
- each unit has its own sight range, which allows to show units more like in RTS, without light effect 
- player can select either to show FOG (more tactical) or LIGHT (more immersion)

## Interception

- some missions on map might be intercepted (type = ufo)
- mini game similar to XCOM is used, but its turn based
- each craft has 4 AP to either move forward, retreat or attack with weapon
- distance between crafts is based on speed of crafts, so with speed of 9 spend 1 AP to move 9 km

## Market

- in general purchasing / selling is same
- item on market may have supplier and limit per month

## Base management

- bases starts as small 4x4, must be upgraded to medium 5x5 and large 6x6
- no scientist / engineers as people, these structure provides capacity for work
- only units are count as living beings for living capacity (now 10 instead of 50)

## Research

- lab facility provides research capacity
- you pay salaries when you invent something
- more clear progress info how many man days left

## Manufacturing

- workshop provide manufacturing capacity, there is no engineers
- you pay salaries when you build something

## Salaries

- lab and workshop does provide capacity for work and cost maintenance
- when project starts it will cost man days of these specialists in monthly invoice
- if no work is done, then no cost
- units cost maintenance / salary either fixed price or based on missions

## Funding and budget

- each month you get invoice for all costs
- facilities in bases are fixed cost
- man-days for science / engineering work is variable depends on usage
- units are partly fixed cost and partly paid per mission
- items ammo replenish after battle / interception 
- craft fuel / rearm / repair is variable cost 
- after that you get money from funding countries

## Lore

- countries for funding
- regions for mission creation
- factions that defines who is who (alien, cult, xcom, mib, etc)
- campaign generate mission every month per faction / region
- each mission may have several objects on world map 
- progres of game are tracked by quests flags
- events may be triggered to generate random effects or to create missions

## Soldiers

- in general unit stats are very similar to XCOM 
- TU are not used, instead there is SPEED 
- all stats are more or less standardized to human in range 5-12 for most

#### Action point system

- each unit has 4 AP during turn
- it can be used to either move or attack
- speed of movement is based on unit speed stat and terrain cost (e.g. 1 AP = 8 tiles with speed of 8)
- weapons use AP to use (pistol 1, rifle 2, grenade 3, etc)
- special actions can be done (kneel 1, overwatch 2, rest 1, etc)
- in general all units have 4 AP, unless there is some special effect or low morale / sanity / wounds

#### Morale and Sanity

- low morale will cause unit to lose AP, and if reach 0 then panic and move randomly (only this battle)
- sanity will cause unit to lose AP until nothing can be done (more permanent)

#### Soldiers experience 

- units gain basic experience points from mission or training at base
- with enough experience points they will gain level up
- on each level up they can be promoted to one of the traits, that provide boost to stats
- stats are more less standardized to human in range 5-12 for most, so e.g. sniper has +2 to aim
- in general human can be max 5 level, and most traits are 3 levels max

#### Soldiers traits and other

- same mechanism as trait for promotion of soldiers are used for:
    - build enemy unit templates
    - wounds (permanent damage after battle)
    - background careers or origin (before they joined xcom)
    - medals (for doing particular mission)
    - effects (temporary effect during battle like frenzy)
    - perks (single trait selected per unit during game by player)
    - transformations (permanent change to unit, like mutant)

#### Wounds and bleeding

- typical human have 6-12 of health points
- game has no bleeding concept, but its much easier to get wounds
- wound is type of "perk" that is hard to or sometimes impossible to heal after battle
- idea is to have more long term wounds and less annoying bleeding

#### Unit inventory 

- unit has inventory:
  - single primary weapon (sword, rifle, rocket launcher, cannon, etc)
  - two secondary weapons (pistol, knife, grenade, medikit, etc)
  - armour
- armour may to some level change this setting (1/2 or 1/1 or 0/3)
- there is no cost of moving between slots, units always have these items during battle, just use them
- if no more ammo then weapon is useless during this battle, and will cost money to replenish after battle

#### Ammunition

- in general game does not have concept of ammo or clips
- weapons have limited ammo, which is more or less 3 clips from original game
- weapons are reloaded after each mission but this is cost to xcom
- same applies to craft weapons
- xcom may select type of ammo before battle (e.g. INC, HE) but this is same weight / cost for xcom

## Aliens

## Pedia

- every pedia page looks same
  - upper section for text
  - lower left section is graphics
  - lower right section is table with tabular data depends on category (e.g. item)
