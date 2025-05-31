1) Resign tileset into single files rather then multiple files

- i need to redesign mechanism of loading data to tilesets from png file. 
- First we need to create a script that will scan for png files in a directory.
- it will then cut the png file into tiles of a specified size. Remember that all tiles has offset of 1 and each tile is 2 pixels from other tiles
- once all files are cut into single tiles, remember about proper naming e.g. farm_000.png, farm_001.png, etc. so in general original name of file + index of tile with 3 numbers
- then redeisgn mechanism of loading tilesets to the game. So all tiles should be stored on single list, with name like file name
- during tiles cutting remember to create a folder of the same name as original file, so if we have farm.png then we will create farm folder and store all tiles in it
- in general in entire game there cannot be 2 files with the same name, as they are loaded into single dictionary based on file name
- all_tiles[key] = tile_object, key does not have .png extension, so if we have farm_000.png then key will be farm_000
- in general all files are 16x16 pixels, so we can use this as a constant, but some files are 32x32 pixels, so we need to handle this as well





2) I need to implement world map mechanics. 

- world map is 2D array of world tiles. Each tile is 16x16 pixels. 
- world tile contains a biome, and may contain a location 
- location is either x-com base, alien base, city, x-com craft, alien ufo, or site
- world map is loaded from tiled file, which contains a 2D array of tiles and its own tileset
- world tile contains information about countries, each tile may be assigned to country
- world tile contains information about region, and each tile belongs to a region or more
- when map is loaded, it should load layer about countries, regions, biomes 
- for regions only every region should have additional calculations based on its tiles owned
- remember when regions are loaded then detects neighbors of each region, so we can calculate borders

2A) world map 
- now add logic to display world map in game, it should be 
- optiomize code for performance 
- allow to use zoom in and out using mouse wheel
- allow drag move using right mouse button

2B) day night cycle
- add mechanism to calculate day and night cycle based on time of day, so map is 240x120 tiles, and 1 day is 1 turn, so 1 month is 30 turns, so every day night should move by 8 tiles
- calculate which world tile is day night based on which day is it of montth, which means in game day would take 1 month in game
- exactly line between day and night should be calculated based on some sinus method to simulate smooth transition, like day / night on earth
- we dont need to calcualte exact time of day, just day and night, so we can use simple logic to calculate it

2C) Events 
- we need to add logic to process day, weeks, months, quarters, and years 
- player just click next turn which is one day, it should process all events, and then move to next day 
- events can be per day, per week, per month, per quarter, or per year, so all must be checked

2D) detection
- allow to explain first concept of detection, so we can detect location in world map
- there are two sides on the map: player and enemy
- each location is either player (x-com base, x-com craft) or enemy (alien base, alien ufo, etc)
- so each side automatically see its own locations, but not enemy locations
- to see enemy location side must first run detection script 
- every location has its own detect_range, and detect_power and cover 
- detection script: 
  - for each location on the map on my side, check if it can detect enemy location in range
  - if it is then reduce their cover by detect_power
  - if remaining cover is less than 0 then location is detected and visible for side
  - if location is detected then it is added to side's detected_locations
  - location may have also cover_recovery which means after this script it recover cover by this amount
  - current cover level cannot be higher than max cover
  - current cover might be negative, which means it is detected for longer period of time

3) integrate demo map

- one file contains map with unit and it can fire at location of map click, and display unit range of sight
- second file contains map filled with blocks, and unit that display line of sight and range of sight, takig into account blocks
- second file also contains pathdinging, so unit can move to location and display path
- second file also contains method to manage larger unit then 1x1 block, so unit can be 2x2 or 3x3 or 4x4, and it can move and display path
- i need to integrate this into single map and look for proper classes to use in BATTLE FOLDER
- generally map contains of 2D array of battle tiles, 
- one battle tile contains of 
  - floor, 
  - wall, 
  - roof, 
  - objects on floor
  - unit 
