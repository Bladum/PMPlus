# Pedia Module

This folder contains classes for the in-game encyclopedia (UFOpedia) system.

## Classes

### TPedia
Main container for the UFOpedia system. Manages and provides access to all pedia entries, categories, and navigation logic.
- **Attributes:** entries (dict), categories (dict)
- **Methods:** __init__(entries=None, categories=None), add_entry(entry), get_entry(pid), list_entries_by_type(type_id), add_category(category), get_category(type_id)

### TPediaEntry
Represents a single entry in the UFOpedia. Stores all relevant data, such as type, name, description, sprite, and related stats.
- **Attributes:** pid, type, name, section, description, sprite, tech_needed, order, related, stats
- **Methods:** __init__(pid, data), is_unlocked(unlocked_techs)

### TPediaEntryType
Represents a type/category of pedia entry. Used for categorizing and managing pedia entries by type.
- **Attributes:** type_id, name, description, icon, order
- **Methods:** __init__(type_id, name, description='', icon='', order=0)

---

See also: `wiki/pedia.md` for more details on the UFOpedia system.
