import platform

import asyncpraw
import discord
from rich.console import Console

from config import DISCORD_TOKEN, REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, PRIVILEGED_USER_IDS
from commands import GetPostCog, TopPostsCog

bot = discord.Bot()
console = Console(width=200)
reddit = asyncpraw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent='Reddit Embed Bot for Discord (by /u/MrNoahMango)',
)

bot.reddit = reddit
bot.console = console


@bot.slash_command(hidden=True)
async def load_cog(ctx: discord.ApplicationContext,
                   cog: discord.Option(description="The cog to load")):
    if ctx.author.id not in PRIVILEGED_USER_IDS:
        await ctx.respond(f"You are not authorized to use this command!")
        return

    try:
        bot.load_extension(f"{cog}")
        await bot.sync_commands()
        await ctx.respond(f"Cog `{cog}` loaded successfully!")
    except Exception as e:
        await ctx.respond(f"Error loading cog `{cog}`: {e}", ephemeral=True)


@bot.slash_command(hidden=True)
async def unload_cog(ctx: discord.ApplicationContext,
                     cog: discord.Option(description="The cog to unload")):
    if ctx.author.id not in PRIVILEGED_USER_IDS:
        await ctx.respond(f"You are not authorized to use this command!")
        return

    try:
        bot.unload_extension(f"{cog}")
        await bot.sync_commands()
        await ctx.respond(f"Cog `{cog}` unloaded successfully!")
    except Exception as e:
        await ctx.respond(f"Error unloading cog `{cog}`: {e}", ephemeral=True)


@bot.slash_command(hidden=True)
async def reload_cog(ctx: discord.ApplicationContext,
                     cog: discord.Option(description="The cog to reload")):
    if ctx.author.id not in PRIVILEGED_USER_IDS:
        await ctx.respond(f"You are not authorized to use this command!")
        return

    try:
        bot.reload_extension(f"{cog}")
        await bot.sync_commands()
        await ctx.respond(f"Cog `{cog}` reloaded successfully!")
    except Exception as e:
        await ctx.respond(f"Error reloading cog `{cog}`: {e}", ephemeral=True)


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
        bot.run(DISCORD_TOKEN)

        bot.load_extension("commands.get_post")
        bot.load_extension("commands.top_posts")

    except KeyboardInterrupt:
        bot.loop.run_until_complete(bot.close())
