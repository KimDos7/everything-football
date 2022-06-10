from tracemalloc import start
from requests import get, request
from bs4 import BeautifulSoup as soup
from datetime import date
import pandas as pd
import time
import random

def get_current_season_data(team):
    standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
    data = get(standings_url)
    s = soup(data.text, features="html.parser")

    standings_table = s.select('table.stats_table')[0]

    standings = pd.read_html(data.text, match="League Table")[0]

    standings = standings.loc[standings['Squad'] == team]

    return standings.values.tolist()[0], list(standings)

def scrape_team_standings(team, year):
    pass

def scrape_one_year(url, random=False):
    data = get(url)
    s = soup(data.text, features="html.parser")

    #obtain the standings table
    standings_table = s.select('table.stats_table')[0]

    links = standings_table.find_all('a')

    links = [l.get("href") for l in links]

    links = list(filter(lambda str: "squads" in str, links))

    #formats the url for each team and creates a list of links to all teams in the table
    team_urls = [f"https://fbref.com{l}" for l in links]

    return team_urls

def scrape_one_team(url, year):
    team_name = url.split("/")[-1].replace("-Stats", "").replace("-", " ")

    print("logging " + team_name + " for year " + str(year))

    url_data= get(url)

    #create matches dataframe for matches a specific team has played
    matches = pd.read_html(url_data.text, match="Scores & Fixtures")[0]

    #obtain shooting data for a specific team
    shootingSoup = soup(url_data.text, features="lxml")
    shoot_link = shootingSoup.find_all('a')
    shoot_link = [l.get("href") for l in shoot_link]

    #filter all links to just obtain the link for shooting stats
    shoot_link = list(filter(lambda str: str != None and 'all_comps/shooting' in str, shoot_link))

    shooting_data = get(f"https://fbref.com{shoot_link[0]}")

    #shooting dataframe

    shooting = pd.read_html(shooting_data.text, match="Shooting")[0]
    shooting.columns = shooting.columns.droplevel()

    #merge two data frames
    wanted_index = ["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]

    checked_index = list(filter(lambda x : x in list(shooting), wanted_index))
    try:
        team_data = matches.merge(shooting[checked_index], on="Date")
    except ValueError:
        pass

    #filtering to only premier league matches and adding columsn season and team to distinguish data
    team_data = team_data[team_data["Comp"] == "Premier League"]
    team_data["Season"] = year
    team_data["Team"] = team_name

    return team_data


def get_everything_standings_from_fbref(starting_year, random=False):
    end_year = date.today().year
    years = list(range(starting_year, end_year))
    standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"

    #an array to hold all the dataframe tables for team data
    all_matches = []

    #loop through as many years as the user specifies
    season_urls = [standings_url]
    print("Obtaining all years' links...")
    for year in years:
        data = get(standings_url)
        s = soup(data.text, features="html.parser")

        prev_season = s.select("a.prev")[0].get("href")
        standings_url = f"https://fbref.com/{prev_season}"
        season_urls.append(standings_url)

    if random:
        return season_urls

    print("Scraping years...")
    i = 0
    for seasons in season_urls:
        team_urls = scrape_one_year(seasons)
        #adding the team dataframe to the overall list
        for urls in team_urls:
            team_data = scrape_one_team(urls, end_year - i)
            all_matches.append(team_data)
            time.sleep(1)
        i += 1

    match_df = pd.concat(all_matches)
    match_df.columns = [c.lower() for c in match_df.columns]
    match_df.to_csv("matches.csv")

def scrape_random(year):
    standing_urls = get_everything_standings_from_fbref(year, True)
    specific_year_url = standing_urls[date.today().year - year]
    team_urls = scrape_one_year(specific_year_url)
    random_url = random.choice(team_urls)
    team_data = scrape_one_team(random_url, year)
    print(team_data)
    print(team_data.sample())
    print(list(team_data))
    return team_data.sample().values.tolist()[0], list(team_data)
