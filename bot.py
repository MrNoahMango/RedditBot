import platform

import asyncpraw
import discord
from rich.console import Console

from config import DISCORD_TOKEN, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET
from commands import register_get_post

bot = discord.Bot()
console = Console()
reddit = asyncpraw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent='Reddit Embed Bot for Discord (by /u/MrNoahMango)',
)


@bot.event
async def on_ready():
    console.log(f"Logged in as {bot.user.name} (ID: {bot.user.id})")


@bot.slash_command(integration_types=[discord.IntegrationType.user_install, discord.IntegrationType.guild_install])
async def ping(ctx: discord.ApplicationContext):
    ctx.respond("Pong!")


if __name__ == '__main__':
    console.log(f"Pycord version: {discord.__version__}")
    console.log(f"PRAW version: {asyncpraw.__version__}")
    console.log(f"Python version: {platform.python_version()}")
    console.log(f"OS: {platform.system()} {platform.release()}")

    try:
        register_get_post(bot, reddit, console)

        bot.run(DISCORD_TOKEN)

    except KeyboardInterrupt:
        bot.loop.run_until_complete(bot.close())
