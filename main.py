import discord 
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import requests
import random
from simpleeval import SimpleEval
import math
from typing import Literal
import asyncio
from datetime import datetime, timedelta
from typing import List

from anime_cache import AniListCache




load_dotenv() 


#stuff for daniel photos

IMAGE_DIR = 'images'
image_paths = [
    os.path.join(IMAGE_DIR, fn)
    for fn in os.listdir(IMAGE_DIR)
    if fn.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
]

anime_cache = AniListCache()

class Client(commands.Bot):

    #stuff that happens on launch (the bot goes online then __ happens)
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        try:
            guild = discord.Object(id=830139678060445707)
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild {guild.id})')
        except Exception as e:
            print(f'Error syncing commands: {e}')

    #stuff that happens whenever a message is sent
    async def on_message(self, message):
       if message.author == self.user:
           return 
       print(f'Message sent by {message.author} in {message.channel}: {message.content}')
       if 'poop' in message.content:
           await message.channel.send ('You said poop LOL')


    #stuff that happens when a message is reacted to
    async def on_reaction_add(self,reaction,user):
        await reaction.message.channel.send(f'you reacted with {reaction.emoji}')
        
           


intents = discord.Intents.default()
intents.message_content = True
token = os.getenv("DISCORD_TOKEN")
client = Client(command_prefix="!",intents=intents)

GUILD_ID = discord.Object(id=830139678060445707)

#commands?
#random daniel photo command
@client.tree.command(name = 'daniel', description='sends a random photo of daniel',guild = GUILD_ID)
async def randDaniel(interaction: discord.Interaction):
    await interaction.response.send_message(file=discord.File(random.choice(image_paths)))

#command that does simple computations
@client.tree.command(name = 'math', description='does math',guild = GUILD_ID)
async def domath(interaction: discord.Interaction, expr: str):
    await interaction.response.send_message(SimpleEval().eval(expr))

@client.tree.command(name="animedetails", description="provides details on an anime", guild=GUILD_ID)
async def animedetails(interaction: discord.Interaction, anime: str):
    await interaction.response.defer()
    # ensure cache is fresh (will no-op if recent)
    await anime_cache.refresh_if_stale()
    if anime not in anime_cache.titles:
        await interaction.followup.send(f"'{anime}' is not in the current top anime list.", ephemeral=True)
        return

    details = await anime_cache.fetch_details(anime)
    if not details:
        await interaction.followup.send(f"Could not fetch details for {anime}.", ephemeral=True)
        return

    title = details["title"].get("english") or details["title"].get("romaji") or anime
    desc = details.get("description") or "No description available."
    score = details.get("averageScore", "N/A")
    episodes = details.get("episodes", "Unknown")
    status = details.get("status", "Unknown")
    site_url = details.get("siteUrl") 
    thumbnail_url = details.get("coverImage", {}).get("large") or details.get("coverImage", {}).get("medium")



    if len(desc) > 300:
        desc = desc[:297] + "..."

    #embed w anime details
    embed = discord.Embed(title = f'{title}', url=f'{site_url}',description=f'Score: {score}\nEpisodes: {episodes}')
    if thumbnail_url:
        embed.set_image(url=thumbnail_url)
    await interaction.followup.send(embed=embed)


@animedetails.autocomplete("anime")
async def animeautocomplete(interaction: discord.Interaction, current: str):
    await anime_cache.refresh_if_stale()  
    suggestions = await anime_cache.get_suggestions(current)
    return [app_commands.Choice(name=s, value=s) for s in suggestions]


client.run(token)



