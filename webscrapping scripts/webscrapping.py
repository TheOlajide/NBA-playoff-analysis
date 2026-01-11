# %%
# installation of beautifulSoup4

#pip install requests beautifulSoup4 selenium

# %%
""""
- we get the range of the years we want to work with and store it in a year variable 

- the years range from 2023 - 2025
"""

years = list(range(2023,2026))

# %%
print (years)

# %%
## url to find the ratings table to scrape the data from the table 
team_ratings_url = "https://www.basketball-reference.com/leagues/NBA_{}_ratings.html"

# %%
import requests

# %%

for year in years:
    url = team_ratings_url.format(year)
    data = requests.get(url)

    with open("team_ratings/{}.html".format(year), "w+", encoding='utf-8') as f:
        f.write(data.text)

# %%
from bs4 import BeautifulSoup

# %%
with open("team_ratings/2024.html", encoding='utf-8') as f:
    page = f.read()

# %%
soup = BeautifulSoup(page, "html.parser")

# %%
soup.find('tr', class_= "over_header").decompose()

# %%
ratings_table= soup.find(id="ratings")

# %%
import pandas as pd

# %%
ratings_2024 =pd.read_html(str(ratings_table))[0]

# %%
ratings_2024

# %% [markdown]
# """
# - using a For loop to get each team rating for each year
# - use beautifulSoup html parser to get the content of the page
# - append the tables into a dataframe
# - write the dataframe into a csv file
# """
# 

# %%
dfs = []

for year in years:
    with open("team_ratings/{}.html".format(year), encoding='utf-8') as f:
        page = f.read()
    soup = BeautifulSoup(page, "html.parser")
    soup.find('tr', class_= "over_header").decompose()
    ratings_table= soup.find(id="ratings")
    rating =pd.read_html(str(ratings_table))[0]
    rating['Year'] = year

    dfs.append(rating)

# %%
rating.head()

# %%
ratings = pd.concat(dfs)

# %%
ratings.tail()

# %%
ratings.to_csv("ratings.csv")

# %% [markdown]
# installation of webdriver to be able to make use of selenium

# %%
#pip install webdriver-manager

# %%
#pip install lxml html5lib

# %%
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# %%
import time

player_stats_url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html"
for year in years:
    url = player_stats_url.format(year)
    
    driver.get(url)
    driver.execute_script("window.scrollTo(1,10000)")
    time.sleep(2)
    
    
    html = driver.page_source
    with open("player/{}.html".format(year), "w+",  encoding='utf-8' ) as f:
        f.write(html)

# %%
from io import StringIO
#import html5lib

# %% [markdown]
# - use of For loop to iterate through the years
# - iterate through the years to get the players table
# - use soup.find to select the class and id of the HTML section to scrape from
# - append information into a data-frame
# - store information in a csv file
# 

# %%
dfs = []

for year in years:
    with open("player/{}.html".format(year), encoding='utf-8') as f:
        page = f.read()
    
    soup = BeautifulSoup( page, "html.parser")
    soup.find('tr', class_= "thead").decompose()
    player_table= soup.find(id="per_game_stats")
    player = pd.read_html(str(player_table))[0]
    player['Year'] = year

    dfs.append(player)

# %%
player.head()

# %%
players = pd.concat(dfs)

# %%
players.head()

# %%
players.to_csv("players.csv")

# %% [markdown]
# - use of For loop to iterate through the years
# - iterate through the years to get the team stats table
# - use soup.find to select the class and id of the HTML section to scrape from
# - append information into a data-frame
# - store information in a csv file
# 

# %%
for year in years:
    team_stats_url="https://www.basketball-reference.com/leagues/NBA_{}.html"
    url = team_stats_url.format(year)
    
    data = requests.get(url)
    
    with open("team_stats/{}.html".format(year), "w+", encoding='utf-8') as f:
        f.write(data.text)

# %%
dfs =[]

for year in years:
    with open("team_stats/{}.html".format(year), encoding='utf-8') as f:
        page = f.read()
         
    soup = BeautifulSoup( page, "html.parser")
    soup.find('tr', class_= "thead").decompose()
    team_table= soup.find(id="divs_standings_E")
    team = pd.read_html(str(team_table))[0]
    team['Year'] = year
    team["Team"] = team["Eastern Conference"]
    del team["Eastern Conference"]
    dfs.append(team)
    
    soup = BeautifulSoup( page, "html.parser")
    soup.find('tr', class_= "thead").decompose()
    team_table= soup.find(id="divs_standings_W")
    team = pd.read_html(str(team_table))[0]
    team['Year'] = year
    team["Team"] = team["Western Conference"]
    del team["Western Conference"]
    dfs.append(team)


# %%
teams = pd.concat(dfs)

# %%
teams

# %%
teams.to_csv("teams_division_standings.csv")

# %%
dfs =[]

for year in years:
    with open("team_stats/{}.html".format(year), encoding='utf-8') as f:
        page = f.read()
         
    soup = BeautifulSoup( page, "html.parser")
    soup.find('tr', class_= "thead").decompose()
    team_table= soup.find(id="confs_standings_E")
    team = pd.read_html(str(team_table))[0]
    team['Year'] = year
    team["Team"] = team["Eastern Conference"]
    del team["Eastern Conference"]
    dfs.append(team)
    
    soup = BeautifulSoup( page, "html.parser")
    soup.find('tr', class_= "thead").decompose()
    team_table= soup.find(id="confs_standings_W")
    team = pd.read_html(str(team_table))[0]
    team['Year'] = year
    team["Team"] = team["Western Conference"]
    del team["Western Conference"]
    dfs.append(team)


# %%
teams = pd.concat(dfs)

# %%
teams

# %%
teams.to_csv("teams_conf_standings.csv")

# %%



