# DynmapBot

### Demonstration
> ```
> .Tr hyesan Kimosaki New_Osaka Kamabo 1.12.21 15.12.21 1.1.22 15.1.22 19.1.22 20.1.22 21.1.22 22.1.22 23.1.22 24.1.22 25.1.22 30.1.22 31.1.22 1.2.22 2.2.22 3.2.22 4.2.22 5.2.22 6.2.22 7.2.22 8.2.22
> ```
![Image GIF](https://cdn.discordapp.com/attachments/646287367501512725/940809737178587236/image.gif)

## Developer Notes
This bot will upload the json files to the 632135935563137026 server in the 719903775556370495 channel managed by Zackaree. 
This primarily serves as a backup for the markup scripts. 

Json markers are downloaded daily. The bot checks hourly and at startup for the files. This is in `./Dependancies/Download.py` 

The 14 day limit on gifs is to prevent the bot from reaching the 8MB limit on uploads. There are better ways to circumvent this.

All commands are case sensitive. This resulted in the need for the TS command. 

## Known Bugs
If a town is named Aurora or Nova, they may not be rendered.  `fixed in flask rewrite`

Bot does not specify if a file cannot be read via an error in the json.  

`./Dependancies/Download.py` Checks for 502 errors, however recent issues have shown checking for a 404 error may prove benefitial. `fixed in flask rewrite`
## Commands
### .TR or .TownRender
Renders specified town(s) on specified date(s). 
Its good to note, with specific dates you can pass the 14 day limit.
```
.Tr [town_name(s)] [server] [date(s)] 
```
> examples
>```
> .Tr Nairobi 2022.4.10 Towny
> .Tr MyTown 2022.4.10 Towny
> .Tr Aurora Houston 1.1.23 2.1.23
> ```

### .Gif
By default, provides a 14 day render from the start date. 

```
.Gif [town_name(s)] [server] [date] 
```
> examples
>```
> .Gif Luxembourg_City Champagne Charleville Paris Orleans Flanders Aurora 23.12.22
> ```

### .TS or .Search or .TSearch
Provides a list of towns from a server which start with the search criteria. 
This has not been made to look good, simply was needed for quick functionality. 

```
.Ts [search_criteria] [server] [date] 
```
> examples
>```
> .Ts a Aurora 1.1.23
> ```
>
>```buildoutcfg
>['a_server', 'aaaaa', 'abidjan', 'african_khazar', 'alhucemas', 'allayoh', 'allayok', 'allium', 'alpha_island', 'alykeriaberg', 'ambonara', 'anchorage', 'anevertos', 'araru', 'aria', 'assassin_cat', 'atlantas', 'awa']
>```

