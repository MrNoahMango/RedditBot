import discord

import asyncpraw
import asyncprawcore

from utils.parser import CommentParser
from utils.embed import CommentEmbed, PostEmbed

from rich.console import Console


def register_get_comment(bot: discord.Bot, reddit: asyncpraw.Reddit):
    @bot.slash_command(name="comment", description="Get a comment from Reddit", integration_types=[discord.IntegrationType.user_install, discord.IntegrationType.guild_install])
    async def get_comment(ctx: discord.ApplicationContext,
                          url: discord.Option(description="Link to the comment")):
        await ctx.defer()

        # noinspection PyUnresolvedReferences
        try:
            comment = await reddit.comment(url=url)
            await comment.load()
        except asyncpraw.exceptions.InvalidURL:
            await ctx.respond("The URL you entered is invalid.")
            return
        except asyncprawcore.NotFound:
            await ctx.respond(f"The comment you entered does not exist.")
            return
        except Exception as e:
            await ctx.respond(f"An error occurred: {e.__class__} {e}")
            return

        parser = await CommentParser.create(comment)

        post_embed = PostEmbed(parser.post)
        comment_embed = CommentEmbed(parser)

        await ctx.respond(embeds=[post_embed, comment_embed])
