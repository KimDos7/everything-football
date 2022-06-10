from tracemalloc import start
from requests import get, request
from bs4 import BeautifulSoup as soup
from datetime import date
import pandas as pd
import time
import random
from lxml import html
import requests
import numpy as np
import re

#Take site and structure html
page = requests.get('https://www.premierleague.com/clubs')
tree = html.fromstring(page.content)

#Using the page's CSS classes, extract all links pointing to a team
linkLocation = tree.cssselect('.indexItem')

#Create an empty list for us to send each team's link to
teamLinks = []

#For each link...
for i in range(0,20):
    
    #...Find the page the link is going to...
    temp = linkLocation[i].attrib['href']
    
    #...Add the link to the website domain...
    temp = "http://www.premierleague.com/" + temp
    
    #...Change the link text so that it points to the squad list, not the page overview...
    temp = temp.replace("overview", "squad")
    
    #...Add the finished link to our teamLinks list...
    teamLinks.append(temp)

#Create empty lists for player links
playerLink1 = []
playerLink2 = []

#For each team link page...
for i in range(len(teamLinks)):
    
    #...Download the team page and process the html code...
    squadPage = requests.get(teamLinks[i])
    squadTree = html.fromstring(squadPage.content)
    
    #...Extract the player links...
    playerLocation = squadTree.cssselect('.playerOverviewCard')

    #...For each player link within the team page...
    for i in range(len(playerLocation)):
        
        #...Save the link, complete with domain...
        playerLink1.append("http://www.premierleague.com/" + playerLocation[i].attrib['href'])
        
        #...For the second link, change the page from player overview to stats
        playerLink2.append(playerLink1[i].replace("overview", "stats"))

#Create lists for each variable
Name = []
Team = []
Age = []
Apps = []
HeightCM = []
WeightKG = []


#Populate lists with each player

#For each player...
for i in range(len(playerLink1)):

    #...download and process the two pages collected earlier...
    playerPage1 = requests.get(playerLink1[i])
    playerTree1 = html.fromstring(playerPage1.content)
    playerPage2 = requests.get(playerLink2[i])
    playerTree2 = html.fromstring(playerPage2.content)

    #...find the relevant datapoint for each player, starting with name...
    tempName = playerTree1.cssselect('div.name')[0].text_content().__str__()
    
    #...and team, but if there isn't a team, return "BLANK"...
    try:
        tempTeam = playerTree1.cssselect('.table:nth-child(1) .long')[0].text_content().__str__()
    except IndexError:
        tempTeam = str("BLANK")
    
    #...and age, but if this isn't there, leave a blank 'no number' number...
    try:  
        str = playerTree1.cssselect('.pdcol2 li:nth-child(1) .info')[0].text_content().__str__().replace('\n', '').strip()
        age = str[12] + str[13]
        tempAge = int(age)
    except IndexError:
        tempAge = float('NaN')

    #...and appearances. This is a bit of a mess on the page, so tidy it first...
    try:
        tempApps = playerTree2.cssselect('.statappearances')[0].text_content()
        tempApps = int(re.search(r'\d+', tempApps).group())
    except IndexError:
        tempApps = float('NaN')

    #...and height. Needs tidying again...
    try:
        tempHeight = playerTree1.cssselect('.pdcol3 li:nth-child(1) .info')[0].text_content()
        tempHeight = int(re.search(r'\d+', tempHeight).group())
    except IndexError:
        tempHeight = float('NaN')

    #...and weight. Same with tidying and returning blanks if it isn't there
    try:
        tempWeight = playerTree1.cssselect('.pdcol3 li+ li .info')[0].text_content()
        tempWeight = int(re.search(r'\d+', tempWeight).group())
    except IndexError:
        tempWeight = float('NaN')


    #Now that we have a player's full details - add them all to the lists
    Name.append(tempName)
    Team.append(tempTeam)
    Age.append(tempAge)
    Apps.append(tempApps)
    HeightCM.append(tempHeight)
    WeightKG.append(tempWeight)

#Create data frame from lists
df = pd.DataFrame(
    {'Name':Name,
     'Team':Team,
     'Age':Age,
     'Apps':Apps,
     'HeightCM':HeightCM,
     'WeightKG':WeightKG})

#Show me the top 3 rows:

df.head()
