
# Welcome to AllienFall

AlienFall is sandbox strategic simulator game. It cover rise and fall of Covert organization managed by player. It start as startup and ends as multiplanetary full scale military organization. It is open ended.

Discord https://discord.gg/7wGAUDUd

![banner](https://github.com/user-attachments/assets/c604e0ce-8e6d-42a4-89c4-6aca1c16a2fa)

This is python based game using mainly agentic ai coding. It 

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
- on each level up they can be promoted to one of the classes, that provide boost to stats
- stats are more less standardized to human in range 5-12 for most, so e.g. sniper has +2 to aim
- in general human can be max 5 level, and most classes are 3 levels max

#### Soldiers perks and other

- same mechanism as classes for promotion of soldiers are used for:
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
