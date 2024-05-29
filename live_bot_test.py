import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta  # Import timedelta
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    bot.loop.create_task(background_task())


@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


@bot.command()
async def meow(ctx):
    await ctx.send("meow meow!!")


@bot.command()
async def ping_user(ctx):
    await ctx.send(f"{ctx.author.mention}, you have been pinged!")


@bot.command()
async def time(ctx):
    current_date = datetime.now()
    await ctx.send(current_date.strftime("%H:%M"))


# Define the provided rotation with all events in UK time zone
rotation_full = [
    ("Infernal Star (Special)", 0),
    ("Lost Souls", 1),
    ("Ramokee Incursion", 2),
    ("Displaced Energy", 3),
    ("Evil Bloodwood Tree (Special)", 4),
    ("Spider Swarm", 5),
    ("Unnatural Outcrop", 6),
    ("Stryke the Wyrm (Special)", 7),
    ("Demon Stragglers", 8),
    ("Butterfly Swarm", 9),
    ("King Black Dragon Rampage (Special)", 10),
    ("Forgotten Soldiers", 11),
    ("Surprising Seedlings", 22),
    ("Hellhound Pack", 23),
]


# Function to find the next special event
def find_next_special_event(local_current_time):
    # Adjust current time to the UK time zone (subtract 2 hours)
    uk_current_time = local_current_time - timedelta(hours=2)

    # Create the schedule for the next 24 hours based on the UK current time
    schedule = []
    start_time = uk_current_time.replace(minute=0, second=0, microsecond=0)

    for i in range(24):
        event_time = start_time + timedelta(hours=i)
        event = rotation_full[event_time.hour % len(rotation_full)]
        schedule.append((event_time, event))

    # Filter out special events
    special_events = [
        (time, event) for time, event in schedule if "Special" in event[0]
    ]

    # Find the next special event
    for event_time, event in special_events:
        if event_time > uk_current_time:
            # Adjust event time back to the user's local time (add 2 hours)
            local_event_time = event_time + timedelta(hours=2)
            return local_event_time, event

    # If no future special events in the next 24 hours, consider the schedule loop
    first_event_time, first_event = special_events[0]
    local_first_event_time = first_event_time + timedelta(hours=2)
    return local_first_event_time, first_event


# Modified background_task for testing
async def background_task():
    await bot.wait_until_ready()
    your_id = "522493027424403456"
    channel_id = "1245476506688425994"
    channel = bot.get_channel(int(channel_id))
    while not bot.is_closed():
        now = datetime.now()
        next_event_time, next_event = find_next_special_event(now)
        # For testing: force a ping as if the event is happening in 5 minutes
        await channel.send(
            f"<@{your_id}>, a special event ({next_event[0]}) is happening in 5 minutes!"
        )
        await asyncio.sleep(60)  # Wait for a minute before checking again


if __name__ == "__main__":
    bot.run(TOKEN)
