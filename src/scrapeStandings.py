from tracemalloc import start
from requests import get, request
from bs4 import BeautifulSoup as soup
from datetime import date
import pandas as pd
import time

def get_standings_from_fbref(seasons=1):
    starting_year = date.today().year
    years = list(range(starting_year, starting_year - seasons, -1))
    standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"

    #an array to hold all the dataframe tables for team data
    all_matches = []

    #loop through as many years as the user specifies
    for year in years:
        data = get(standings_url)
        s = soup(data.text, features="html.parser")

        #obtain the standings table
        standings_table = s.select('table.stats_table')[0]

        links = standings_table.find_all('a')

        links = [l.get("href") for l in links]

        links = list(filter(lambda str: "squads" in str, links))

        #formats the url for each team and creates a list of links to all teams in the table
        team_urls = [f"https://fbref.com{l}" for l in links]

        prev_season = s.select("a.prev")[0].get("href")
        standings_url = f"https://fbref.com/{prev_season}"

        for team_url in team_urls:
            #isolating the team name from the given api call
            team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")

            print("logging " + team_name + " for year " + str(year))

            url_data= get(team_url)

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
            try:
                team_data = matches.merge(shooting[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on="Date")
            except ValueError:
                continue

            #filtering to only premier league matches and adding columsn season and team to distinguish data
            team_data = team_data[team_data["Comp"] == "Premier League"]
            team_data["Season"] = year
            team_data["Team"] = team_name

            #adding the team dataframe to the overall list
            all_matches.append(team_data)
            time.sleep(1)

    match_df = pd.concat(all_matches)
    match_df.columns = [c.lower() for c in match_df.columns]
    match_df.to_csv("matches.csv")


def obtain_standings():
    url = "https://www.soccerstats.com"
    page = soup(get(url).content, "html.parser")

    print(page)