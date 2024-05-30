import discord
from discord.ext import commands
from datetime import datetime, timedelta
from functions.utils import find_next_special_event  # Import necessary functions

# Function to register all bot commands
def register_commands(bot):
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
            color=discord.Color.green()
        )
        embed.add_field(name="Next Special Event",
                        value=f"**{next_event[0]}** is happening at **{next_event_time.strftime('%H:%M')}**.",
                        inline=False)
        embed.add_field(name="Following Special Event",
                        value=f"**{next_next_event[0]}** will happen in **{int(hours)}h {int(minutes)}m** at **{next_next_event_time.strftime('%H:%M')}**.",
                        inline=False)

        await ctx.send(embed=embed)
