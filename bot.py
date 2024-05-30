import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from functions.tasks import background_task  # Import the background_task function from functions
from functions.commands import register_commands  # Import the register_commands function from functions

# Load environment variables from the .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Set up bot intents and command prefix
intents = discord.Intents.default()
intents.message_content = True

# Initialize the bot with the specified command prefix and intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Register commands defined in functions/commands.py
register_commands(bot)

# Event that triggers when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    # Start the background task
    bot.loop.create_task(background_task(bot))

# Run the bot using the token from the .env file
if __name__ == "__main__":
    bot.run(TOKEN)
