import discord
from discord.ext import commands

import asyncpraw
import asyncprawcore

from utils.parser import PostParser
from utils.views import EmbedNavigator

from rich.console import Console


def register_top_posts(bot: discord.Bot, reddit: asyncpraw.reddit.Reddit, console: Console):
    @bot.slash_command(name="top_posts", description="Browse top posts from a subreddit", integration_types=[discord.IntegrationType.user_install, discord.IntegrationType.guild_install])
    async def reddit_top_posts(ctx: discord.ApplicationContext,
                               subreddit_name: discord.Option(description="Subreddit name")):
        await ctx.defer()

        try:
            subreddit = await reddit.subreddit(subreddit_name, fetch=True)
        except asyncprawcore.Forbidden:
            await ctx.respond("The subreddit you entered is private.", ephemeral=True)
            return
        except asyncprawcore.Redirect:
            await ctx.respond("The subreddit you entered does not exist.", ephemeral=True)
            return
        except Exception as e:
            await ctx.respond(f"An error occurred: {e.__class__} {e}")
            console.log(f"Error in subreddit {subreddit_name}: {e}")
            return

        posts = []
        async for post in subreddit.top(limit=5):
            posts.append(await PostParser.create(post))

        if not posts:
            await ctx.respond("No posts found.", ephemeral=True)
            return

        # Create the navigation view
        view = EmbedNavigator(posts, ctx.author)
        view.message = await ctx.respond(embed=await view.create_embed(), view=view, ephemeral=False)
