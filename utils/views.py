import discord
from discord.ui import View, Button

from .parser import PostParser, CommentParser
from .embed import PostEmbed, CommentEmbed

from typing import List


class EmbedNavigator(View):
    def __init__(self, posts: List[PostParser], author):
        super().__init__(timeout=60)
        self.posts = posts
        self.index = 0
        self.message = None
        self.author = author

    async def create_embed(self):
        post: PostParser = self.posts[self.index]

        embed = PostEmbed(post)
        sub_text = embed.footer.text
        sub_icon = embed.footer.icon_url
        embed.set_footer(
            text=f"{sub_text} ⋅ Post {self.index + 1}/{len(self.posts)}",
            icon_url=sub_icon
        )

        return embed

    # async def interaction_check(self, interaction: discord.Interaction) -> bool:
    #     return interaction.user.id == self.author.id

    @discord.ui.button(label="⬅")
    async def previous(self, _: Button, interaction: discord.Interaction):
        self.index = (self.index - 1) % len(self.posts)
        await interaction.response.edit_message(embed=await self.create_embed(), view=self)

    @discord.ui.button(label="➡")
    async def next(self, _: Button, interaction: discord.Interaction):
        self.index = (self.index + 1) % len(self.posts)
        await interaction.response.edit_message(embed=await self.create_embed(), view=self)

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        if self.message:
            await self.message.edit(view=self)


class PostCommentViewer(View):
    def __init__(self, post: PostParser):
        super().__init__(timeout=120)
        self.comments = post.comments

        self.index = 0

    async def generate_embed(self):
        return CommentEmbed(await CommentParser.create(self.comments[self.index]))

    @discord.ui.button(label="⬅")
    async def previous(self, _: Button, interaction: discord.Interaction):
        self.index = (self.index - 1) % len(self.comments)
        await interaction.response.edit_message(embed=await self.generate_embed(), view=self)

    @discord.ui.button(label="➡")
    async def next(self, _: Button, interaction: discord.Interaction):
        self.index = (self.index + 1) % len(self.comments)
        await interaction.response.edit_message(embed=await self.generate_embed(), view=self)

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        if self.message:
            await self.message.edit(view=self)


class PostViewer(View):
    def __init__(self, post: PostParser):
        super().__init__(timeout=120)
        self.post = post
        self.index = 0

    async def generate_embed(self):
        return PostEmbed(self.post, self.index)

    # @discord.ui.button(label="⬅")
    # async def previous(self, _: Button, interaction: discord.Interaction):
    #     self.index = (self.index - 1) % len(self.comments)
    #     await interaction.response.edit_message(embeds=await self.generate_embed(), view=self)
    #
    # @discord.ui.button(label="➡")
    # async def next(self, _: Button, interaction: discord.Interaction):
    #     self.index = (self.index + 1) % len(self.comments)
    #     await interaction.response.edit_message(embeds=await self.generate_embed(), view=self)

    @discord.ui.button(emoji="<:comment:1363552669733748948>")
    async def comments(self, _: Button, interaction: discord.Interaction):
        comment_view = PostCommentViewer(self.post)
        await interaction.respond(f"**Comments on {self.post.title}:**", embed=await comment_view.generate_embed(), view=comment_view, ephemeral=True)

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        if self.message:
            await self.message.edit(view=self)
