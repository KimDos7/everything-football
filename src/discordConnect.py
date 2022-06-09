import os
import discord

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

print("Getting client...")

client = discord.Client()

print("Printing client...")
print(client)

@client.event
async def on_ready():
    print("Entered...")
    print('We have logged in as {0.user}'.format(client))
    #print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(TOKEN)