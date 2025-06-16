# API Reference

This document provides a concise, table-based API reference for Python classes configured via YAML, following the style of the OpenXcom ruleset documentation. Each section corresponds to a class, with a table listing all configurable parameters, example values, and descriptions.

---

## Example: `Item` Class

| API Name      | Example Value      | Description                                      |
|--------------|-------------------|--------------------------------------------------|
| id           | "STR_LASER_RIFLE" | Unique string identifier for the item.            |
| type         | "weapon"          | The category/type of the item.                    |
| costBuy      | 30000             | Purchase cost in in-game currency.                |
| weight       | 6                 | Weight of the item (affects unit encumbrance).    |
| power        | 85                | Damage or effect strength (context-dependent).    |
| clipSize     | 20                | Number of uses/shots before reloading.            |
| special      | ["auto", "laser"] | Special item tags or features.                    |

*Descriptions are based on class docstrings, YAML comments, or inferred from context. OXCE-specific or extended parameters should be highlighted as needed.*

---

## Example: `Facility` Class

| API Name      | Example Value      | Description                                      |
|--------------|-------------------|--------------------------------------------------|
| id           | "STR_LAB"         | Unique string identifier for the facility.        |
| buildCost    | 150000            | Construction cost in in-game currency.            |
| buildTime    | 26                | Time to build (in days).                          |
| upkeep       | 3000              | Monthly maintenance cost.                         |
| size         | [1, 1]            | Facility size (width, height) on the base grid.   |
| provides     | ["research"]      | Capabilities or bonuses provided by the facility. |

---

## TUnitType
Represents a type of unit with its stats, combining race, traits, and items. Used as a template for units, not directly by the player.

| API Name     | Example Value                | Description                                      |
|--------------|-----------------------------|--------------------------------------------------|
| pid          | "xcom_soldier"              | Unique identifier for the unit type.              |
| name         | "XCOM Soldier"              | Display name of the unit.                        |
| race         | "human"                     | Race identifier.                                 |
| sprite       | "unit_sectoid_soldier_1"    | Sprite or image reference.                       |
| rank         | 0                           | Rank value.                                      |
| traits       | ["soldier"]                 | List of trait identifiers.                       |
| armour       | "arm_sectoid_soldier" or ["arm_sectoid_soldier"] | Armour configuration.            |
| primary      | "item_plasma_rifle" or ["item_plasma_rifle"] | Primary weapon configuration.      |
| secondary    | [] or [["item_alien_grenade", null, null]] | Secondary weapon configuration.   |
| score_dead   | 5                           | Score for killing this unit.                     |
| score_alive  | 20                          | Score for capturing this unit alive.             |
| items_dead   | ["corpse_human"]            | Items dropped on death.                          |
| items_alive  | ["live_xcom_soldier"]       | Items dropped if alive.                          |
| ai_ignore    | false                       | AI ignore flag.                                  |
| vip          | false                       | VIP flag.                                        |
| drop_items   | false                       | Drop items on death flag.                        |
| drop_armour  | false                       | Drop armour on death flag.                       |

---

## TRace
Represents a race (type of unit) and its basic stats, abilities, and AI behavior. Used as a template for unit creation and stat calculation.

| API Name         | Example Value         | Description                                      |
|------------------|----------------------|--------------------------------------------------|
| pid              | "human"              | Unique identifier for the race.                   |
| name             | "Human"              | Display name of the race.                        |
| description      | "Standard human..."  | Human-readable description.                       |
| sprite           | "race_human"         | Sprite or image reference.                        |
| size             | 1.0                  | Size multiplier.                                 |
| speed            | 6                    | Movement speed.                                  |
| health           | 3                    | Base health.                                     |
| energy           | 7                    | Base energy.                                     |
| strength         | 3                    | Base strength.                                   |
| reaction         | 4                    | Base reaction.                                   |
| melee            | 3                    | Base melee skill.                                |
| aim              | 4                    | Base aim.                                        |
| psi              | 2                    | Base psi skill.                                  |
| bravery          | 5                    | Base bravery.                                    |
| sanity           | 7                    | Base sanity.                                     |
| sight            | [20, 10]             | Sight range (day, night).                        |
| sense            | [3, 2]               | Sense range.                                     |
| cover            | [0, 0]               | Cover values.                                    |
| is_big           | false                | Is the race large?                               |
| is_mechanical    | false                | Is the race mechanical?                          |
| gain_experience  | true                 | Can gain experience?                             |
| health_regen     | 0                    | Health regeneration per turn.                    |
| sound_death      | null                 | Sound played on death.                           |
| corpse_image     | null                 | Corpse image reference.                          |
| aggression       | 0.0                  | AI aggression.                                   |
| intelligence     | 0.0                  | AI intelligence.                                 |
| immune_panic     | false                | Immune to panic?                                 |
| immune_pain      | false                | Immune to pain?                                  |
| immune_bleed     | false                | Immune to bleeding?                              |
| can_run          | true                 | Can run?                                         |
| can_kneel        | true                 | Can kneel?                                       |
| can_sneak        | true                 | Can sneak?                                       |
| can_surrender    | false                | Can surrender?                                   |
| can_capture      | false                | Can be captured?                                 |
| spawn_on_death   | null                 | Entity spawned on death.                         |
| avoids_fire      | false                | Avoids fire?                                     |
| spotter          | 0                    | Spotter role value.                              |
| sniper           | 0                    | Sniper role value.                               |
| sell_cost        | 0                    | Sell cost.                                       |
| female_frequency | 0.0                  | Female frequency.                                |
| level_max        | 0                    | Max level.                                       |
| level_train      | 0                    | Training level.                                  |
| level_start      | 0                    | Starting level.                                  |

---

## wounds.yaml (Data Structure)
Wounds are defined as entries under the `wounds` key. Each wound has parameters as shown below. No direct Python class, but used for unit traits and effects.

| API Name      | Example Value         | Description                                      |
|---------------|----------------------|--------------------------------------------------|
| name          | "Medal for..."       | Name of the wound/trait.                         |
| sprite        | "trait_injury_broken"| Sprite reference.                                |
| races         | ["human", "hybrid"]  | Races affected.                                  |
| type          | 5                    | Wound type (5 = permanent).                      |
| description   | "Medal for..."       | Description.                                     |
| stats         | {aim: -3, ...}       | Stat modifications.                              |
| recovery_time | 30                   | Recovery time in days.                           |

---

## TPedia (pedia.yaml)
Represents the UFOpedia system. Each entry is defined under the `pedia` key. Entry structure is likely handled by a class such as `TPediaEntry`.

| API Name     | Example Value         | Description                                      |
|--------------|----------------------|--------------------------------------------------|
| type         | 4                    | Entry type/category.                             |
| name         | "Laser Pistol"       | Display name.                                    |
| section      | "Weapons"            | Section/category.                                |
| description  | "A basic..."         | Description text.                                |
| sprite       | "pedia_laser_pistol" | Sprite reference.                                |
| tech_needed  | ["laser_tech"]        | Required technologies.                           |
| order        | 2500                 | Display order.                                   |

---

## TQuest
Represents a quest or flag for tracking game progress. Used to manage progress in game instead of using research.

| API Name      | Example Value         | Description                                      |
|---------------|----------------------|--------------------------------------------------|
| key           | "promotion_A"        | Quest key.                                       |
| name          | "Promotion A"        | Quest name.                                      |
| description   | "Achieve the..."     | Description of the quest.                        |
| pedia         | "pedia_quest..."     | Encyclopedia entry.                              |
| value         | 10                   | Value/weight for progress.                       |
| quests_needed | ["quest_promotion_B"]| Quests required to complete.                     |
| tech_needed   | ["tech_promotion_A"] | Technologies required to complete.               |
| completed     | false                | Whether the quest is completed.                  |

---

## Unit Traits, Transformations, Ranks, Promotions, Origins (YAML Data Structure)
These YAML files define traits, transformations, ranks, promotions, and origins for units. Each entry is a configuration object with the following possible fields:

| API Name      | Example Value         | Description                                      |
|---------------|----------------------|--------------------------------------------------|
| name          | "Sniper"             | Name of the trait/transformation/rank/etc.        |
| sprite        | "trait_promotion_sniper" | Sprite reference.                           |
| races         | ["human", "orc"]      | Races affected.                                  |
| type          | 0, 1, 2, 3, 5         | Type/category (see comments in YAML).             |
| description   | "A master of..."      | Description.                                      |
| stats         | {health: 1, ...}      | Stat modifications.                               |
| recovery_time | 4                     | Recovery time (if applicable).                    |
| transfer_time | 0                     | Transfer time (if applicable).                    |
| cost          | 30                    | Cost (if applicable).                             |
| tech_needed   | ["tech_class_sniper"] | Required technologies (if applicable).            |
| service_needed| []                    | Required service (if applicable).                 |
| min_level     | 0                     | Minimum level (if applicable).                    |
| max_level     | 3                     | Maximum level (if applicable).                    |

> **Note:** This structure also applies to medals (special awards, `medals.yaml`) and temporary effects (`effects.yaml`). All these files use the same trait configuration format for units.

---

## World, Region, Country, and Biome Configuration (YAML Data Structures)

### worlds.yaml
Defines worlds (planets/maps) available in the game.

| API Name    | Example Value         | Description                                      |
|-------------|----------------------|--------------------------------------------------|
| name        | "Earth"              | Name of the world.                               |
| description | "The home planet..." | Description of the world.                        |
| size        | [80, 40]              | Size of the map (width, height).                 |
| map         | "earth_map.tmx"      | Map file reference.                              |
| countries   | true                  | Whether countries are present.                   |
| bases       | true                  | Whether bases are allowed.                       |
| factions    | true                  | Whether factions are present.                    |
| regions     | true                  | Whether regions are present.                     |
| tech_needed | ["mars_terraforming"] | Technologies required to unlock.                 |

---

### regions.yaml
Defines regions (continents/areas) on the world map.

| API Name         | Example Value         | Description                                      |
|------------------|----------------------|--------------------------------------------------|
| name             | "Europe"             | Name of the region.                              |
| is_land          | true                  | Is the region land?                              |
| description      | "A continent..."     | Description of the region.                       |
| sprite           | "regions_001"        | Sprite reference.                                |
| color            | "#FF00FF"            | Color code for the region.                       |
| mission_weight   | 18                    | Weight for mission selection.                    |
| base_cost        | 800                   | Cost to build a base in this region.             |
| service_provided | []                    | Services provided.                               |
| service_forbidden| []                    | Services forbidden.                              |

---

### countries.yaml
Defines countries on the world map.

| API Name         | Example Value         | Description                                      |
|------------------|----------------------|--------------------------------------------------|
| name             | "USA"                | Name of the country.                             |
| description      | "The United States..."| Description of the country.                      |
| sprite           | "countries_001"      | Sprite reference.                                |
| color            | "#FF00FF"            | Color code for the country.                      |
| funding          | 50                    | Monthly funding provided.                        |
| funding_cap      | 100                   | Maximum possible funding.                        |
| initial_relation | 5                     | Initial diplomatic relation.                     |
| service_provided | []                    | Services provided.                               |
| service_forbidden| []                    | Services forbidden.                              |

---

### biomes.yaml
Defines biomes (terrain types) for world map tiles.

| API Name    | Example Value         | Description                                      |
|-------------|----------------------|--------------------------------------------------|
| map_id      | 1                    | Unique map tile ID.                              |
| type        | "water"              | Biome type (e.g., water, land).                  |
| name        | "Ocean"              | Name of the biome.                               |
| sprite      | "biomes_001"         | Sprite reference.                                |
| description | "A vast expanse..."  | Description of the biome.                        |
| terrains    | {farmland: 20, ...}  | Dictionary of terrain types and weights.          |

---

## UFO Scripts, UFOs, Sites, and Cities (YAML Data Structures)

### ufo_script.yaml
Defines mission scripts for UFOs, controlling their behavior on the world map.

| API Name | Example Value | Description |
|----------|--------------|-------------|
| name     | "Patrol"     | Name of the script. |
| desc     | "Enemy will patrol..." | Description of the script. |
| steps    | {land: 6, ...} | Sequence of actions (optional, varies by script). |

---

### ufos.yaml
Defines enemy UFOs/craft and their properties.

| API Name       | Example Value         | Description                                      |
|----------------|----------------------|--------------------------------------------------|
| name           | "Car"                | Name of the UFO/craft.                           |
| pedia          | "pedia_cultist_car"  | Pedia entry reference.                           |
| sprite         | "craft_cultist_car"  | Sprite reference.                                |
| marker         | "cultist"            | Marker type.                                     |
| size           | 1                    | Size category.                                   |
| health         | 15                   | Hit points.                                      |
| speed          | 6                    | Movement speed.                                  |
| shield         | 0                    | Shield value.                                    |
| shield_regen   | 0                    | Shield regeneration per turn.                    |
| damage         | 5                    | Weapon damage.                                   |
| rate           | 4                    | Rate of fire.                                    |
| range          | 1                    | Weapon range.                                    |
| accuracy       | 0.5                  | Weapon accuracy.                                 |
| fire_sound     | "sfx_cultist_car"    | Sound played when firing.                        |
| hunter         | true                 | Is this a hunter craft?                          |
| hunt_bravery   | 0.8                  | Bravery threshold for hunting.                   |
| missile_power  | 0                    | Number of facilities destroyed.                  |
| cover          | 2                    | Cover value.                                     |
| cover_change   | 0                    | Change in cover.                                 |
| radar_range    | 2                    | Radar detection range.                           |
| radar_power    | 5                    | Radar detection power.                           |
| score_complete | 0                    | Score for completing mission.                    |
| score_destroy  | 10                   | Score for destroying craft.                      |

---

### sites.yaml
Defines special sites on the world map. (Currently only empty objects, but can be extended.)

| API Name | Example Value | Description |
|----------|--------------|-------------|
| (site id)| {}           | Site configuration (extend as needed). |

---

### cities.yaml
Defines cities, their properties, and associated terrains.

| API Name    | Example Value         | Description                                      |
|-------------|----------------------|--------------------------------------------------|
| name        | "London"             | Name of the city.                                |
| size        | 5                    | Size category.                                   |
| description | "The capital..."     | Description of the city.                         |
| terrains    | {urban_2: 2, ...}    | Mapping of terrain types to weights.              |

---

## Organizations, Factions, Events, and Campaigns (YAML Data Structures)

### organization.yaml
Defines player organization levels and their properties.

| API Name | Example Value | Description |
|----------|--------------|-------------|
| name     | "Covert Actions" | Name of the organization level. |
| description | "A small, secretive..." | Description of the organization. |
| sprite   | "org_blank"   | Sprite reference. |
| pedia    | "pedia_org_ca" | Pedia entry reference. |
| quests   | ["investigate_anomaly"] | List of quest IDs for this level. |

---

### factions.yaml
Defines factions in the game.

| API Name   | Example Value         | Description                                      |
|------------|----------------------|--------------------------------------------------|
| name       | "XCOM"               | Name of the faction.                             |
| pedia      | "pedia_faction_xcom" | Pedia entry reference.                           |
| description| "The Extraterrestrial Combat Unit..." | Description of the faction. |
| id         | 0                    | Faction ID.                                      |
| tech_start | []                   | Starting technologies.                           |
| tech_end   | []                   | Ending technologies.                             |

---

### events.yaml
Defines events that can occur in the game.

| API Name   | Example Value         | Description                                      |
|------------|----------------------|--------------------------------------------------|
| name       | "Rat Attack"         | Name of the event.                               |
| description| "A rat has attacked you!" | Description of the event.                   |
| sprite     | "event_rat_attack"   | Sprite reference.                                |
| tech_needed| []                   | Required technologies.                           |
| regions    | {europe: 2, ...}     | Regions and weights.                             |
| is_city    | true                 | Is the event city-specific?                      |
| day_start  | 1                    | Start day.                                       |
| day_random | 120                  | Random day offset.                               |
| day_end    | 10000                | End day.                                         |
| score      | -50                  | Score impact.                                    |
| funds      | 100                  | Funds impact.                                    |
| items      | ["item_rat"]         | Items involved.                                  |
| chance     | 0.2                  | Chance of event.                                 |
| qty_max    | 1                    | Maximum quantity.                                |

---

### campaign.yaml
Defines campaigns and their properties.

| API Name   | Example Value         | Description                                      |
|------------|----------------------|--------------------------------------------------|
| name       | "Resefaction H"      | Name of the campaign.                            |
| score      | 0                    | Starting score.                                  |
| faction    | "aliens"             | Faction for the campaign.                        |
| tech_start | []                   | Starting technologies.                           |
| tech_end   | []                   | Ending technologies.                             |
| regions    | {north_america: 10, ...} | Regions and weights.                        |
| missions   | [{ufo: 'alien_small_scout', count: 1, timer: 9}, ...] | List of mission dicts. |

---

## Calendar (YAML Data Structure)
Defines the campaign calendar, including start/end dates and monthly event scheduling.

| API Name  | Example Value         | Description                                      |
|-----------|----------------------|--------------------------------------------------|
| start_day | "1997-01-01"         | Campaign start date (YYYY-MM-DD).                |
| end_day   | "2004-12-30"         | Campaign end date (YYYY-MM-DD).                  |
| months    | [ ... ]              | List of month configuration blocks.               |

Each month block contains:

| API Name  | Example Value         | Description                                      |
|-----------|----------------------|--------------------------------------------------|
| month_min | 0                    | Minimum month (offset from campaign start).       |
| weights   | {event: 1, ...}      | Event type weights for random selection.          |
| qty_min   | 1                    | Minimum number of events.                         |
| qty_max   | 2                    | Maximum number of events.                         |
| events    | 3                    | Number of events (if specified).                  |

---

*This documentation is auto-generated from YAML and Python sources. Update both code and YAML to keep this documentation in sync.*
