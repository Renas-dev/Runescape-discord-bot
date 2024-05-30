import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
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


@bot.command()
async def event(ctx):
    now = datetime.now()
    next_event_time, next_event = find_next_special_event(now)
    next_next_event_time, next_next_event = find_next_special_event(next_event_time + timedelta(minutes=1))
    time_to_next_next_event = next_next_event_time - now

    # Convert timedelta to a readable format
    hours, remainder = divmod(time_to_next_next_event.total_seconds(), 3600)
    minutes, _ = divmod(remainder, 60)

    embed = discord.Embed(
        title="Upcoming Special Events",
        color=discord.Color.green()  # Green color
    )
    embed.add_field(name="Next Special Event",
                    value=f"**{next_event[0]}** is happening at **{next_event_time.strftime('%H:%M')}**.",
                    inline=False)
    embed.add_field(name="Following Special Event",
                    value=f"**{next_next_event[0]}** will happen in **{int(hours)}h {int(minutes)}m** at **{next_next_event_time.strftime('%H:%M')}**.",
                    inline=False)

    await ctx.send(embed=embed)


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


async def background_task():
    await bot.wait_until_ready()
    your_id = "522493027424403456"
    channel_id = "1245476506688425994"
    channel = bot.get_channel(int(channel_id))
    notified_events = set()  # Set to keep track of notified event times

    while not bot.is_closed():
        now = datetime.now()
        next_event_time, next_event = find_next_special_event(now)
        # Calculate the time difference to the next event
        time_to_next_event = next_event_time - now

        # If the next event is within the next 5 minutes and not already notified, send a reminder
        if 0 < time_to_next_event.total_seconds() <= 300 and next_event_time not in notified_events:
            embed = discord.Embed(
                title="Special Event Reminder",
                description=f"<@{your_id}>, **a special event** **{next_event[0]}** **is happening in 5 minutes!**",
                color=discord.Color.green()  # Green color
            )
            embed.add_field(name="Check Details",
                            value="[Double check here](https://runescape.wiki/w/Wilderness_Flash_Events)",
                            inline=False)
            await channel.send(embed=embed)
            notified_events.add(next_event_time)  # Add the event time to the notified set

            # Wait until the event has passed to reset the notification
            while datetime.now() < next_event_time + timedelta(minutes=1):
                await asyncio.sleep(10)

            # Find the next special event after the current one
            new_now = datetime.now()
            next_next_event_time, next_next_event = find_next_special_event(new_now)
            time_to_next_next_event = next_next_event_time - new_now

            # Convert timedelta to a readable format
            hours, remainder = divmod(time_to_next_next_event.total_seconds(), 3600)
            minutes, _ = divmod(remainder, 60)

            embed = discord.Embed(
                title="Upcoming Special Event",
                color=discord.Color.green()  # Green color
            )
            embed.add_field(name="Next Special Event",
                            value=f"**{next_next_event[0]}** will happen in **{int(hours)}h {int(minutes)}m** at **{next_next_event_time.strftime('%H:%M')}**.",
                            inline=False)
            await channel.send(embed=embed)
        else:
            await asyncio.sleep(10)  # Check every 10 seconds for accuracy


if __name__ == "__main__":
    bot.run(TOKEN)
