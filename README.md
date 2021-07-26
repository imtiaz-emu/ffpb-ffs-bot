# FFS-BOT

FFS-BOT is a python selenium based script to go and fetch match data from [Fantasy Football Scout](https://www.fantasyfootballscout.co.uk/) match stats page.

#### Prerequisites:
  - Python version 3.7+ 
  - Google Chrome
  - ChromeWebdriver

#### How to run?

  - Create a virtualenv (optional but recommended)
    It'll be helpful for installing dependencies in a isolated place. Then activate the virtualenv to run the script. Otherwise, you need to install the libraries from `requirement.txt` file manually and run the script. 
  - Inside project directory: create a `.env` file. Put 3 environment variables: 
    1. FFS_USERNAME=<YOUR_FFS_USERNAME>
    2. FFS_PASSWORD=<YOUR_FFS_PASSWORD>
    3. WEBDRIVER_PATH=<YOUR_CHOMEDRIVER_PATH>
  - Remember: _Google Chrome_ version and _ChromeDriver_ version must be same. Current Google Chrome is 92. So, download ChromeDriver version 92 and install.     
  - From project directory run: `python3 ffs_bot.py 212123`. Here, 212123 = the match ID from which you want to extract the data.
  - Results will be written in `match_stats.json` file.


#### Implementation

![Sample Player Stats of a Match](https://i.ibb.co/YW6KGyn/player-Stats-FFS.png)

- First login to FFS site using credentials from `.env` file. Then sleep for 3 seconds to load the webpage.
- Next, we initialize every players data with empty `Hash/Dictionary`
- Then for each player, go through Tab by Tab. Tabs definition can be found on `constants.py` file. 
- For each tab, go through every row of the table, find the row associated with Player Name, then extract and assign the data to empty player stats. 

#### To Extend

- Currently, we're extracting data from 3 tabs. If you want to collect data from other tabs, define the tab info in `constants.py` file.
- For additional/new tab data, initialize the `build_player_stats` of `player_stats.py` file with new dictionary key-value pair.
- In `player_stats.py` file, extend `player` function with for new `tab_type`
 
##### Example Contribution 

**constants.py**
```python
constants = {
  '#player-tabs-2': 'involvement',
  '#player-tabs-7': 'keeping',
  '#player-tabs-11': 'expected',
  '#player-tabs-1': 'fantasy' # < Added new tab >
}
```

**player_stats.py**

Initialize empty data dictionary:
```python
def build_player_stats(page_source):
  ...... other codes
  categories = ['touches', 'passes', 'expected', 'keeping', 'assist_potential', 'goal_threat', 'fantasy'] # newly added dict key
  ...... other codes 
```

Define new extraction method:
```python
def player(page_source, stats_type, stats):
  if stats_type == 'involvement':
    stats = involvement(page_source, stats)
  elif stats_type == 'expected':
    stats = expected(page_source, stats)
  elif stats_type == 'keeping':
    stats = keeping(page_source, stats)
  # Added following 2 lines to extract info from fantasy tab
  elif stats_type == 'fantasy':
    stats = fantasy(page_source, stats)

  return stats
```

Write extract data method:
```python
def fantasy(page_source, stats):
  for indx, row_data in enumerate(page_source.find_elements_by_css_selector('td')):
    if indx == 0:
      stats['fantasy'][X] = row_data.text.strip()
    if indx == 3:
      stats['fantasy'][Y] = row_data.text.strip()
  # Here X, Y can be 'goals', 'assists' etc.
  return stats
```

License
----

FFPB


**Free Software, Hell Yeah!**

