# This example requires the 'message_content' intent.
from dotenv import load_dotenv
import os
import discord
from osu_api.osuapi import get_me
from osu_api.osuapi import get_user
from discord.ext import commands


# from osu_api import osuapi


def get_token():
    load_dotenv(".env")
    token = os.getenv("DISCORD_BOT_TOKEN")

    if token is None:
        raise ValueError("Token not found check the .env file")

    return token


TOKEN: str = get_token()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
# client = discord.Client(intents=intents)


# @client.event
# async def on_ready():
#     print(f"We have logged in as {client.user}")
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.command()
async def osu(ctx, arg: str = None):
    if not arg:
        await ctx.send(embed=get_me())

    elif arg:
        await ctx.send(embed=get_user(arg))


bot.run(TOKEN)
