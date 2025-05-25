
## [Skill]()

- skill is addon to unit that boost stats in specific way
- skill is generic mechanism used in many different ways:
  - as **promotion** of soldier for experience
  - as special skill for soldier to simulate their **background origins** before XCOM
  - as way to build enemy units from **classes**
  - as way to **transform** soldiers other than promotion via experience (e.g. cyborg)
  - as way to simulate permanent **wounds** from battles e.g. lost leg
  - as way to simulate **temporary effects** during battle e.g. bloodlust
  - as way to simulate special awards on battlefields aka **medals**
  - as way to simulate **perks**, which are manually selected additional skill, very narrow

#### [Promotion]() 

- Soldier once get enough experience he can collect new skill
- Same skill can be acquired multiply times
- Each skill gives some permanent bonus to stats ( e.g. sniper +2 aim)
- Some skill may be acquired only once or few times
- Some skill may be required for items

skill for xcom:
- scout
- soldier
- sniper
- medic
- heavy
- assault
- ninja
- commander
- psychic
- engineer
- pilot

#### [Transformations]()

- transformation is very similar to promotion but it's not used when level up
- transformation are expensive, long term changes to unit stats
- they usually require resources, money, time and facility in base

#### [Classes]()

- Same mechanism is used to build unit templates for battles
- typical enemy unit is build from: 
  - race
  - level, that defines set of skill e.g. soldier + soldier + engineer
  - armour, primary weapon, secondary weapons
- other than that it works for enemy same way like promotion for x-com

#### [Background origins]()

- Each xcom soldier might have a special one time skill 
- this represents background of soldier 
- origins are only used during creation of unit, they cannot be acquired by promotion

#### [effects]()

- effects is temporary skill assigned to soldier to simulate special effect like bleeding, bloodlust, panic etc
- effects are removed from solder after battle ends

#### [Medals]()

- soldier may acquire medal for completing special mission 
- medal is one time skill and cannot be got another way
- it may boost stats in special way

#### [Wounds]()

- soldier if hit may get a wound 
- there is no concept of bleeding in game
- after battle each would, may cause a permanent would that would cripple the soldier e.g. lost leg
- woulds may or may not be treatable or very long time

#### [Perks]()

- special ability that is assigned to soldier
- usually it should add one major advantage and one disadvantage
- perks are not permanent, they can be removed, but only one can be assigned to soldier at any time
- perks required special level of unit
- this is similar to perks in Fallout game 
- soldier may need to spent some time to activate perk