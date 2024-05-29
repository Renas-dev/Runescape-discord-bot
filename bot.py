import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Define the intents
intents = discord.Intents.default()
intents.message_content = True  # Enable the message_content intent

# Create a new bot instance with the specified intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Command: Ping
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')


@bot.command()
async def meow(ctx):
    await ctx.send('meow meow!!')


# Run the bot with the token
bot.run(TOKEN)
