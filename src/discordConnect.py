import os
import discord
from soupsieve import match
import scrapeStandings
from dynamoStorage import setUserFavorite
import csv
import random
import pandas as pd

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

print("Getting client...")

client = discord.Client()

print("Printing client...")

@client.event
async def on_ready():
    print("Entered...")
    print('We have logged in as {0.user}'.format(client))
    #print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #handles the logic with a !scrape command
    if message.content.startswith('!scrape'):
        print("Scrape command received!")
        user = message.author.name
        discriminator = message.author.discriminator

        scrapeMsg = message.content.split(" ")

        print(scrapeMsg)
        if scrapeMsg[1] == "set":
            await message.channel.send("Updating Info!")
            change = scrapeMsg[2]
            if change == "FavTeam":
                messageSplit = scrapeMsg[3].split("-")
                newTeam = " ".join(messageSplit)
                print(setUserFavorite.updateUserFavoriteTeam(user, discriminator, newTeam))
            await message.channel.send("Updated!")
        elif scrapeMsg[1] == "get":
            await message.channel.send("Getting Info!")
            info = scrapeMsg[2]
            if info == "CurrentTeam":
                await message.channel.send(setUserFavorite.getUserFavoriteTeam(user, discriminator))
            if info == "CurrentSeason":
                team = setUserFavorite.getUserFavoriteTeam(user, discriminator)
                data, headers = scrapeStandings.get_current_season_data(team)
                await message.channel.send(combine_header_data(data, headers, False))

        else:

            await message.channel.send("Scraping your request...")

            #League, The league year, type they want to scrape
            data, headers = handle_scrape_parsor(scrapeMsg[1], scrapeMsg[3], "None", scrapeMsg[2])

            line = combine_header_data(data, headers)

            await message.channel.send('Match Stats:\n>>> {}'.format(line))

#called when a user wants to scrape some data
def handle_scrape_parsor(league, type, team, year=2022):
    if type == "random":
        return scrapeStandings.scrape_random(int(year))

def combine_header_data(data, headers, reversed=True):
    one_stat_per_line = ""
    output = list(zip(headers, data))

    if reversed:
        output = reversed(output)
    for e in output:
        if e[0] == 'Unnamed: 0':
            continue
        one_stat_per_line += e[0].capitalize() + ": " + str(e[1]) + "\n"

    return one_stat_per_line


#grabbing csv header names
def grab_csv_headers(csv_file):

    # creating an object of csv reader
    # with the delimiter as ,
    df = pd.read_csv('matches.csv')

    list_of_col_names = list(df.columns)

    return list_of_col_names
 

client.run(TOKEN)