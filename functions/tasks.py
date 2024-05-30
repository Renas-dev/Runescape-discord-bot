import discord
from datetime import datetime, timedelta
import asyncio
from functions.utils import find_next_special_event  # Import necessary functions

# Define the background task
async def background_task(bot):
    await bot.wait_until_ready()
    your_id = "522493027424403456"
    channel_id = "1245476506688425994"
    channel = bot.get_channel(int(channel_id))
    notified_events = set()  # Set to keep track of notified event times

    while not bot.is_closed():
        now = datetime.now()
        next_event_time, next_event = find_next_special_event(now)
        time_to_next_event = next_event_time - now

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

            while datetime.now() < next_event_time + timedelta(minutes=1):
                await asyncio.sleep(10)

            new_now = datetime.now()
            next_next_event_time, next_next_event = find_next_special_event(new_now)
            time_to_next_next_event = next_next_event_time - new_now

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
