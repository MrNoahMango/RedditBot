import discord

import asyncpraw
import asyncprawcore

from utils.parser import PostParser
from utils.views import PostViewer

from rich.console import Console


def register_get_post(bot: discord.Bot, reddit: asyncpraw.Reddit, console: Console):
    @bot.slash_command(name="post", description="Get a post from Reddit", integration_types=[discord.IntegrationType.user_install, discord.IntegrationType.guild_install])
    async def get_post(ctx: discord.ApplicationContext,
                       url: discord.Option(description="Link to the post")):
        await ctx.defer()

        # noinspection PyUnresolvedReferences
        try:
            submission = await reddit.submission(url=url)
        except asyncpraw.exceptions.InvalidURL:
            await ctx.respond("The URL you entered is invalid.")
            return
        except asyncprawcore.NotFound:
            await ctx.respond(f"The post you entered does not exist.")
            return
        except Exception as e:
            await ctx.respond(f"An error occurred: {e.__class__} {e}")
            return

        post = await PostParser.create(submission)

        view = PostViewer(post)
        view.message = await ctx.respond(embed=await view.generate_embed(), view=view, ephemeral=False)
