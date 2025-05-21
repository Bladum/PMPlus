# [Economy]()

## [Marketplace]()

### [Purchasing]()

- entries which are available on the market to be purchased
- each item supposed to have supplier
- supplier diplomacy status impact price and availability
  - you cannot purchase from enemies
  - prices from allies are lower by 25%
  - prices from neutral are normal
- you can purchase
  - new units
  - new crafts
  - new items
  - new craft items

### [Selling]()

- in general every item has selling point
- crafts ARE not items, but be scrapped ??
- units ARE NOT items, but be scrapped ??
- if item does not have price sell it cannot tbe sold 

### [Black market ]()

- to agreed how to do it
- buy things from other factions but at cost of losing score
- they are very expensive

## [Manufacturing]()

- this is done in very similar way like in XCOM
- main difference there is no engineers concept, instead each facility has its own production capacity
- workshop gives capacity for 25 Man Days and this will be total TIME used on project
- salaries for workshop are paid on daily basis, only when are being used
- facilities always pays for maintenance
- manufacturing only cost for salary if something is being build, e.g. time to build
- cost of items (both time, resources, money) are fixed

## [Funding]()

- countries funds xcom based on its founding base and score in its territory
- each country has its own funding level (starts with 5) and funding budget (money)
- if country has good score per month it will get +1 level to fund more
- if country has bad score per month it will get -1 level to fund less
- if country will reach max level of 10, that would be its max funding
- if country reach level of 0, it will be removed from xcom
- infiltration missions will reduce funding level by some number
- countries may start with different funding level, default is 5
- alien base in country may reduce funding level by 1 per month
- country leaving xcom does not mean losing game, means it will not fund xcom anymore

### [Salaries and invoices in base]()

- alternative method is that you got invoice for each facility how it was used this month 
  - total 200 MD of science
  - total 100 MD of engineers 
  - total 48 MD of soldiers missions
  - total fuel for crafts
  - and based on this you are charged on monthly basis
- in addition, cost to maintain facilities and crafts 
- scientist and engineers have flat fee, they just pay for man days
- units may have their own upkeep cost based on their level
  - humans from 0 to 5 level, cost is per level
  - tanks do not promote, fixed cost per action



## [Losing game]()

- losing base, even last one, does not mean game over
- if you have money to build new base then its ok 
- if you lose all countries funding xcom, then you will not be supported by government, but its game over
- if you have huge debt, than will have to get loan to pay it, but interest will be bigger and bigger
- large negative score per month means only less funding
- some mission / research / quests in game may trigger some cut scenes like winning with aliens
- game is open ended, more like a sandbox
- in time game becomes more and more harder due to increasing number of campaigns
- the longer you survive the better it gets, 
- the only think you can win is to get as good total score as possible at the end, and how far you went

Example
- in basic mod there is only faction - aliens from mars
- if you win cydonia battle then it will disable this faction missions, making in practice end of game
- game can display cut scene you won with aliens (faction), but game does not end

## [Research]() 

- This is done very similar way like in XCOM
- main difference is that there is no concept of scientists, instead each facility has its own research capacity
- laboratory gives capacity for 25 Man Days and this will be total TIME used on project
- research only cost for salary if something is being researched, e.g. time to research
- so if you have cap of 25 scientist and use 20 at the moment, you will pay for 20 for this day
- there is no monthly salary for scientists, only daily salary when used
- cost of research is random for all research and setup when game starts at aprox 50-150% of baseline
- research is streamlined, if something cost 50MD and random value would be 54MD, then game will display progress in %
- there are no other hidden mechanism like chance to discover or number of scientists etc...
- some research required to have item in the same base or facility or service or another research

Things which are done differently:
- in general, you dont need to create item from battlefield to allow to research it
- if there are items only for this (aka story) then we will directly unlock research for player
- so there is no need to create items only for story purpose
