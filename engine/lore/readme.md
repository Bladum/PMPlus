# Lore Module

This folder contains classes for managing the lore, campaigns, events, factions, missions, organizations, and quests in the game. Each class is responsible for a specific aspect of the game's narrative and progression systems.

## TCalendar
Manages the in-game calendar, campaign scheduling, and event checks.
- **Attributes:** year, month, day, total_days, campaign_months
- **Methods:** set_start_date(), get_date(), advance_days(), generate_monthly_campaigns(), daily_campaign_check(), on_day(), on_week(), on_month(), on_quarter(), on_year()

## TCampaign
TCampaign represents a set of missions for a specific faction in a specific region. It is created by the calendar and has a start date, end date, and list of missions, limited by research status. It has a goal to achieve, when the alien will score points.
- **Attributes:** pid, name, score, objective, faction, tech_start, tech_end, regions, missions
- **Methods:** __init__()

## TCampaignStep
TCampaignStep defines mission generation rules for a specific game month. It specifies how many campaigns/events are generated and their weights for a given month.
- **Attributes:** month, qty_min, qty_max, events, weights
- **Methods:** __init__()

## TEvent
Represents an event in the game that can affect the player or trigger missions.
- **Attributes:** pid, name, description, sprite, tech_needed, regions, is_city, month_start, month_random, month_end, qty_max, chance, score, funds, items, units, crafts, facilities, ufos, sites, bases

## TEventEngine
Manages random events in the game.

## TFaction
Represents a faction in the game, which can own missions and locations.
- **Attributes:** pid, name, description, id, aggression, pedia, sprite, tech_start, tech_end

## TMission
Represents a mission created by a campaign, with deployment and tech requirements.
- **Attributes:** ufo, site, base, count, chance, timer, tech_start, tech_end, deployments

## TOrganization
Represents a player organization level, with unlock requirements and quests.
- **Attributes:** key, name, description, sprite, pedia, quests, quests_needed, tech_needed, unlocked

## TQuest
Represents a quest or flag for tracking game progress.
- **Attributes:** key, name, description, pedia, value, quests_needed, tech_needed, completed

## TQuestEngine
Manages quests in the game.

## QuestManager
Tracks quest and organization progress, unlocks new content, and provides progress metrics.
- **Attributes:** quests, organizations, completed_techs, completed_quests
- **Methods:** update_quests(), update_organizations(), get_progress(), unlock_new_content(), get_unlocked_organizations(), get_locked_organizations()

---

- All classes follow project documentation and testing standards.
- See test/ subfolder for unit tests covering all public methods and attributes.
- For API details, see wiki/API.yml.
