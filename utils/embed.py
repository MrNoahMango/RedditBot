import discord

from .parser import PostParser, CommentParser


class PostEmbed(discord.Embed):
    def __init__(self, post: PostParser, media_index=0, include_media: bool = True):
        if post.text:
            description = f"{post.text}\n\n<:upvote:1363552719834579145> {post.score} | <:comment:1363552669733748948> {post.comment_count}"
        else:
            description = f"<:upvote:1363552719834579145> {post.score} | <:comment:1363552669733748948> {post.comment_count}"

        super().__init__(
            title=post.title,
            description=description,
            url=post.url,
            author=discord.EmbedAuthor(
                name=post.author.name,
                url=post.author.url,
                icon_url=post.author.avatar_url
            ),
            footer=discord.EmbedFooter(
                post.subreddit.name,
                post.subreddit.icon_url
            ),
            colour=discord.Color.from_rgb(255, 69, 0)
        )

        if include_media:
            self.set_image(url=post.media.urls[media_index])

        if post.media.is_video:
            self.add_field(name="Can't play video", value="")


class CommentEmbed(discord.Embed):
    def __init__(self, comment: CommentParser):
        super().__init__(
            author=discord.EmbedAuthor(
                name=comment.author.name,
                url=comment.author.url,
                icon_url=comment.author.avatar_url
            ),
            description=comment.text,
            url=comment.url,
            footer=discord.EmbedFooter(
                icon_url=comment.subreddit.icon_url,
                text=f"{comment.subreddit.name}"
            ),
            colour=discord.Color.from_rgb(255, 69, 0)
        )

        self.add_field(
            name="",
            value=f"<:upvote:1363552719834579145> {comment.score} | <:comment:1363552669733748948> {comment.reply_count}")
