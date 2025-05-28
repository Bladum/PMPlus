# Welcome to AlienFall

AlienFall is a turn-based strategy game with tactical combat and sandbox/simulation elements. 
Players manage a covert organization from its humble beginnings as a startup to its evolution into a multiplanetary military power. 
The game is open-ended with no fixed victory conditions.

[Join our Discord](https://discord.gg/7wGAUDUd)

![banner](https://github.com/user-attachments/assets/c604e0ce-8e6d-42a4-89c4-6aca1c16a2fa)

## TL;DR

AlienFall features:
- Strategic layer with global operations (similar to X-COM's Geoscape)
- Tactical combat with squad-based missions
- Base management and resource allocation
- Technology research to unlock new capabilities
- Open-ended gameplay with no fixed win/loss conditions
- Sandbox and simulation elements

## Design Principles 

### Core Philosophy

- Inspired by X-COM but not a clone of OpenXcom
- Developed using AI Agentic Coding as a practical experiment
- Open source, non-commercial project (likely MIT license)
- Supports total conversion mods rather than smaller mod fragments
- Documentation in wiki format designed to be human-readable and AI-compatible

### Game Mechanics 

- Generic, reusable game systems with flexible customization options
- Emphasis on reliability and intuitive design
- Balanced complexity across different game systems
- No external scripting language (at least initially)
- Shared mechanics for multiple purposes:
  - Traits system for ranks, medals, mutations, perks, wounds, etc.
  - Quest system for research, events, missions, and lore
  - Unified ammo system for weapons and vehicles
  - Comprehensive salary system for all operations

### Use of Generative AI

- Limited use for player-visible content
- Extensive use for background/procedural content
- Future plans for player-accessible AI content generation for modding

### User Interface 

- Functional modern UI prioritized over visual effects
- 16×16 pixel art tiles, upscaled to 32×32
- Streamlined UI with minimal screen nesting
- Notification system instead of excessive popups
- Information disclosed based on research/lore progress

### Financial System

- FinOps layer for detailed cost management
- Variable costs based on usage rather than fixed expenses
- Monthly invoicing with multiple revenue streams
- Dynamic cost structures:
  - Pay-for-work scientific and engineering staff
  - Mission-based reloading and maintenance
  - Craft repair, rearm, and refueling costs
  - Personnel training and recovery expenses
  - Mission-based soldier compensation
- Strategic resource management for raids and missions

### Geoscape 

- Units assigned directly to craft
- Day-based turn system (1 turn = 1 day)
- Tactical movement on world map
- Consistent top-down 2D perspective across all game layers
- Detection mechanics based on radar power and cover values
- Multiple planetary environments (Earth, Moon, Mars)
- Earth-based funding from nations, with region-based missions across all worlds

### Basescape 

- Compact bases (starting at 4×4, expandable to 6×6)
- Generic capacity-based facilities (science, engineering, living quarters, etc.)
- Flexible craft storage independent of specific hangars
- Abstract workforce capacity instead of individual scientists/engineers
- Pay-for-use facility model with maintenance costs

### Battlescape 

- Line-of-sight mechanics prioritized over lighting systems
- Consistent unit mechanics for players and AI
- Simplified day/night cycle with binary states
- Streamlined inventory system:
  - Armor slot
  - Primary weapon slot
  - Up to 3 secondary weapon slots
- Promotion-based character progression
- Battle-limited ammunition with post-mission resupply
- Reduced micromanagement for improved gameplay flow

### Lore and Narrative 

- Morally ambiguous player organization
- Covert operations with varying levels of public exposure
- Score-based public funding with alternative income sources
- Compatible with X-Com Files mod lore elements
- Progressive organizational development
- Quest-based progression separate from research
- Escalating difficulty through various mechanisms:
  - Increasing mission frequency
  - Specialized rather than generalized soldier development
  - Permanent/long-term injury mechanics

## FAQ 

### What is AlienFall?
AlienFall is a configurable game built in Python, inspired by classic strategy games like UFO: Enemy Unknown. It's designed to be modded through text files rather than function as a general engine.

### What does the name and logo represent?
"Alien" represents any outsider or opponent, not necessarily extraterrestrial. "Fall" represents the process of defeating these opponents. The tick logo symbolizes covert infiltration, persistence, and survival—starting small but ultimately bringing down larger adversaries. In Polish culture, it represents both the alien concept and causing a downfall.

### Is it a clone of X-COM?
While inspired by X-COM (UFO: Enemy Unknown), AlienFall introduces its own mechanics and systems. It borrows successful elements but isn't constrained by the need to replicate the original.

### How is it related to OpenXcom's X-Com Files mod?
AlienFall aims to support all features required by X-Com Files in some form, providing a similar experience even if implementation differs.

### Why make another X-COM-like game?
The project is primarily focused on agentic coding development rather than just creating a game. It integrates three elements:
- Documentation in markdown format
- YAML-based mod configuration
- Python game engine

### Who does the player represent?
The player leads a covert organization through five evolutionary stages:
1. **Covert Actions**: A secretive startup investigating anomalies
2. **Covert Bureau**: A government-affiliated shadow agency
3. **Covert Command**: A global strike force with elite units
4. **Covert Division**: A militarized planetary defense organization
5. **Covert Enclave**: An interplanetary power with its own agenda

The organization's only imperative is survival, allowing for moral flexibility in player choices.

### Why use Python?
- Excellent AI integration capabilities
- PySide6/Qt provides cross-platform GUI support
- Sufficient performance for this type of game
- Option for C++ modules where performance is critical
- Supports collaborative development with AI assistance

### How does AI-assisted game development differ?
- AI can simultaneously work on documentation, mods and engine code
- Development typically begins with documentation rather than code
- Allows focus on game design rather than implementation details

### How are mods supported?
Mods are implemented through configuration files, with an emphasis on total conversions rather than small modifications.

### How are features prioritized for inclusion?
Features are evaluated based on AI implementability, development feasibility, and player enjoyment rather than strict adherence to design documents.

### What makes the game "open-ended"?
There's no definitive ending—quests and technology may trigger cinematic events but don't conclude the game. Each playthrough varies based on procedurally generated campaigns.

### What makes this a strategic game?
- Global operational management
- Base and resource administration
- Technology research and development

### What makes this a tactical game?
- Turn-based aerial interception system
- Squad-level ground combat

### What makes this a sandbox game?
The absence of fixed victory conditions and the ability to initiate missions freely create an open play environment.

## Differences from X-COM: UFO Defense

### World Map
- 2D tile-based Earth representation (90×45 grid)
- Support for additional planets with unique environments
- Tile-based biomes with region and country assignments
- City-scale locations occupying entire tiles
- One mission per tile at any time

### Detection System
- Bases and craft have detection range and power ratings
- Enemy operations have cover power and recovery rates
- Missions become detected when cover is reduced to zero
- Detected missions allow player interaction

### Location Types
- Alien bases: Permanent installations that grow and generate missions
- Sites: Static temporary missions that expire over time
- UFOs: Mobile missions with scripted behaviors that can be intercepted

### Time Management
- One game day per turn
- Simplified day/night cycle lasting one month
- Standard 30-day months

### Battle System
- Tile-based terrain with map blocks
- Single-layer design with height variations
- Map blocks sized at 15×15 or multiples
- Variable battle sizes (4×4 to 6×6 blocks)
- Diverse mission objectives beyond elimination

### Graphics
- 16×16 pixel symbolic art upscaled to 32×32

### Line of Sight
- Simplified partial coverage system rather than LOFT
- Distance and cover-based accuracy
- Terrain height influencing cover and visibility

### Visibility System
- Binary day/night states
- Optional light sources on map elements
- Unit-specific sight ranges
- Player-selectable FOG or LIGHT display modes

### Interception
- Turn-based aerial combat
- 4 Action Points per craft
- Movement distance based on craft speed
- Tactical positioning and weapon engagement

### Economy
- Similar buying/selling mechanics to original X-COM
- Supplier-based market with monthly quantity limits

### Base Management
- Size-based base progression (4×4 to 6×6)
- Capacity-based facility functionality
- Abstract workforce rather than individual personnel
- Reduced living space requirements

### Research
- Capacity-based laboratory system
- Pay-per-result scientific funding
- Clear progress tracking

### Manufacturing
- Capacity-based workshop system
- Production-based payment system

### Financial System
- Monthly invoice system
- Fixed facility maintenance costs
- Variable workforce expenses
- Mission-based unit compensation
- Post-operation resupply costs
- Variable vehicle maintenance expenses
- Country-based funding following expenses

### Lore System
- Country-based funding
- Region-based mission generation
- Faction-defined alignments
- Monthly campaign-based mission generation
- Quest-based progress tracking
- Event-triggered effects and missions

### Unit Management
- XCOM-like stats with Speed replacing Time Units
- Standardized 5-12 stat range for humans

### Action System
- 4 Action Points per unit
- Movement and attack options
- Speed-based movement distance
- Weapon-specific AP costs
- Special action options
- Status effects limiting available AP

### Psychological Factors
- Battle-limited morale affecting AP availability
- Persistent sanity system with long-term effects

### Experience System
- Mission and training-based experience gain
- Level progression with trait selection
- Specialized stat improvements
- 5-level maximum for humans
- 3-level trait caps

### Trait System
- Unified system for multiple functions:
  - Enemy templates
  - Permanent injuries
  - Character backgrounds
  - Achievement medals
  - Temporary effects
  - Selectable perks
  - Unit transformations

### Health System
- 6-12 health points for typical humans
- No active bleeding mechanic
- Persistent wound system with difficult or impossible healing
- Long-term injury management

### Inventory System
- Simplified loadout:
  - Primary weapon slot
  - Secondary weapon slots (up to 3)
  - Armor slot
- Armor-based slot configuration variations
- No slot-swapping costs during battle
- Battle-limited ammunition

### Ammunition System
- No physical clips/magazines
- Battle-limited ammunition (equivalent to ~3 X-COM clips)
- Post-mission automatic resupply at cost
- Applies to both infantry and vehicle weapons
- Pre-battle ammunition type selection
