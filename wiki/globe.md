# [Geoscape]()

## Detection
## Interception

### [World]() 

- world is based on tiles, earth is 90x45 tiles, each is aprox 500km
- game may have multiple worlds, each with its own size, biomes etc but only on earth xcom can build bases
- each tile of world map has a biome
- each tile of world might be owned by country (24 of them) that funds xcom activities
- each tile of world MUST be part of region, which are used to create missions

### [Other Worlds]()
- earth
- moon
- mars
- underworld
- another dimension

Each world may have different size and bioms

### [Countries]()

- there are 24 countries on earth that funds xcom
- each country has its own funding level, may be part of xcom or not depends on score in her territory
- on some worlds like underground there is no countries
- countries are only to represent people and civil, not organization
- countries owns tiles, but not ufo's or bases
- there might be some mission that target mainly country status towards XCOM (infiltration)
- score reporting is managed per country
- reporting per country is lower than per region as not all tiles are owned by country

### [Regions]() 

- each tile must be assigned to a region, only one
- regions help to manage missions, as mission always start with region
- region and missions might have some weights
- score reporting is managed per region
- regions usually are mix of water and land

### [Biomes]()

- biom is type of natural environment available on single tile of world
- this is used to select which terrain will be used on battlefield
- some battles ignore bioms terrain, just force its own
- biom FOREST can be used to simulate FOREST, WET FOREST, HIGH FOREST, JUNGLE as terrain

Biomes: 
  - ocean
  - sea
  - grassland / farmland
  - desert
  - mountains
  - arctic
  - tundra
  - jungle

There might be events that do modify Biome of a tile to something else e.g. biomas or star ghosts or mars terraformation.

### [World Time]()

- game on world is turn based 
- one turn = 1 day, 30 days = month and 12 months = year
- day and night cycle is done by changing the light level of the world map, speed is 3 tiles per day
- there is only either day or night, nothing in between
- special events are triggered every day, every monday, every month, every quarter, every year

### [Locations]()

on world map you can find
- cities
- xcom bases
- alien bases
- xcom craft
- alien ufo
- sites (static missions)
- portal to another world for crafts only