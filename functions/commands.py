import discord
from discord.ext import commands
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from functions.utils import find_next_special_event
import json


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

    @bot.command()
    async def vis(ctx):
        user_agent = "discord-bot-rune-goldberg-combinations"
        url = "https://runescape.wiki/api.php?action=parse&page=Forum:Discord_collaboration:Rune_Goldberg_Combinations&format=json"

        try:
            response = requests.get(url, headers={"User-Agent": user_agent})
            response.raise_for_status()

            data = response.json()
            parse_text = data["parse"]["text"]["*"]
            soup = BeautifulSoup(parse_text, 'html.parser')

            table = soup.find("table", {"class": "wikitable"})
            if not table:
                await ctx.send("Could not find the combination table.")
                return

            rows = table.find_all("tr")
            best_combination = []
            for row in rows[2:]:  # Skip the header rows
                cols = row.find_all("td")
                if len(cols) >= 6:
                    slot_1_rune = cols[0].text.strip()
                    slot_2_rune = cols[3].text.strip()
                    best_combination.append(f"Slot 1: {slot_1_rune}")
                    best_combination.append(f"Slot 2: {slot_2_rune}")

            best_combination_text = "\n".join(best_combination) if best_combination else "No combinations found."

            embed = discord.Embed(
                title="Best Rune Goldberg Combinations",
                color=discord.Color.blue()
            )
            embed.add_field(name="Combination", value=best_combination_text, inline=False)

            await ctx.send(embed=embed)

        except requests.exceptions.RequestException as e:
            await ctx.send(f"Failed to retrieve data: {e}")

    @bot.command()
    async def merchant(ctx):
        user_agent = "discord-bot-daily-merchant-rotation"
        url = "https://runescape.wiki/api.php?format=json&action=parse&prop=text&disablelimitreport=1&text={{Travelling%20Merchant/api|format=json}}"

        try:
            response = requests.get(url, headers={"User-Agent": user_agent})
            response.raise_for_status()

            data = response.json()
            parse_text = data["parse"]["text"]["*"]
            soup = BeautifulSoup(parse_text, 'html.parser')

            # Extract the JSON string from the HTML content
            json_str = soup.find("p").text.strip()

            # Parse the JSON data
            merchant_data = json.loads(json_str)
            items = merchant_data["items"]

            # Build the merchant loot message
            merchant_loot = []
            for item in items:
                item_name = item["name"]
                item_cost = item["cost"]
                merchant_loot.append(f"**{item_name}**: {item_cost} coins")

            merchant_loot_text = "\n".join(merchant_loot) if merchant_loot else "No merchant loot found."

            embed = discord.Embed(
                title="**Daily Merchant Loot**",
                color=discord.Color.blue()
            )
            embed.add_field(name="**Today's Loot**", value=merchant_loot_text, inline=False)

            await ctx.send(embed=embed)

        except requests.exceptions.RequestException as e:
            await ctx.send(f"Failed to retrieve data: {e}")