import asyncpraw
from asyncpraw.models.comment_forest import CommentForest


class AuthorParser:
    def __init__(self, author: asyncpraw.reddit.Redditor | None):
        self.author = author

    @classmethod
    async def create(cls, author: asyncpraw.reddit.Redditor | None):
        if author:
            # noinspection PyProtectedMember
            if not author._fetched:
                await author.load()

        return cls(author)

    @property
    def raw_name(self) -> str:
        if self.author:
            return self.author.name
        else:
            return "deleted"

    @property
    def name(self) -> str:
        return f"u/{self.raw_name}"

    @property
    def url(self):
        if self.author:
            return f"https://www.reddit.com/user/{self.raw_name}"
        else:
            return None

    @property
    def avatar_url(self):
        if self.author:
            return self.author.icon_img
        else:
            return "https://www.redditstatic.com/shreddit/assets/snoovatar-back-64x64px.png"

    @property
    def is_deleted(self):
        return self.author is None


class SubredditParser:
    def __init__(self, subreddit: asyncpraw.reddit.Subreddit):
        self.subreddit = subreddit

    @classmethod
    async def create(cls, subreddit: asyncpraw.reddit.Subreddit):
        # noinspection PyProtectedMember
        if not subreddit._fetched:
            await subreddit.load()

        return cls(subreddit)

    @property
    def raw_name(self):
        return self.subreddit.display_name

    @property
    def name(self):
        return self.subreddit.display_name_prefixed

    @property
    def url(self):
        return f"https://www.reddit.com{self.subreddit.permalink}"

    @property
    def icon_url(self):
        return self.subreddit.community_icon

    @property
    def public_description(self):
        return self.subreddit.public_description

    @property
    def description(self):
        return self.subreddit.description


class PostMediaParser:
    def __init__(self, post: asyncpraw.reddit.Submission):
        self.post = post

    # noinspection PyProtectedMember
    @classmethod
    async def create(cls, post: asyncpraw.reddit.Submission):
        if not post._fetched:
            await post.load()

        return cls(post)

    @property
    def is_video(self):
        return self.post.is_video

    @property
    def media_count(self):
        return len(self.urls)

    @property
    def urls(self):
        media = []

        if self.post.is_self:
            return media  # Skip text posts

        # Direct image
        if self.post.url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            media.append(self.post.url)

        # Reddit-hosted video
        elif self.post.is_video and self.post.media:
            media.append(self.post.media['reddit_video']['fallback_url'])

        # Gallery
        elif hasattr(self.post, "gallery_data") and hasattr(self.post, "media_metadata"):
            for item in self.post.gallery_data['items']:
                media_id = item['media_id']
                media_info = self.post.media_metadata.get(media_id)
                if media_info and media_info['e'] == 'Image':
                    media.append(media_info['s']['u'].replace('&amp;', '&'))

        # External media
        elif not self.post.is_self:
            media.append(self.post.url)

        return media


class PostParser:
    def __init__(self,
                 post: asyncpraw.reddit.Submission,
                 author: AuthorParser,
                 subreddit: SubredditParser,
                 media: PostMediaParser,
                 comments: CommentForest):
        self.post = post
        self.author = author
        self.subreddit = subreddit
        self.media = media
        self.comments = comments

    # noinspection PyProtectedMember
    @classmethod
    async def create(cls, post: asyncpraw.reddit.Submission):
        if not post._fetched:
            await post.load()

        if post.author:
            if not post.author._fetched:
                await post.author.load()

        if not post.subreddit._fetched:
            await post.load()

        await post.comments.replace_more()

        author = await AuthorParser.create(post.author)
        subreddit = await SubredditParser.create(post.subreddit)
        media = await PostMediaParser.create(post)
        comments = await post.comments()

        return cls(post, author, subreddit, media, comments)

    @property
    def title(self):
        return self.post.title

    @property
    def text(self):
        return self.post.selftext

    @property
    def url(self):
        return f"https://www.reddit.com{self.post.permalink}"

    @property
    def score(self):
        return self.post.score

    @property
    def comment_count(self):
        return self.post.num_comments


class CommentParser:
    def __init__(self,
                 comment: asyncpraw.reddit.Comment,
                 author: AuthorParser,
                 subreddit: SubredditParser,
                 post: PostParser):
        self.comment = comment
        self.author = author
        self.subreddit = subreddit
        self.post = post

    # noinspection PyProtectedMember
    @classmethod
    async def create(cls, comment: asyncpraw.reddit.Comment):
        if not comment._fetched:
            await comment.load()

        if comment.author:
            if not comment.author._fetched:
                await comment.author.load()

        if not comment.subreddit._fetched:
            await comment.subreddit.load()

        if not comment.submission._fetched:
            await comment.submission.load()

        author = await AuthorParser.create(comment.author)
        subreddit = await SubredditParser.create(comment.subreddit)
        post = await PostParser.create(comment.submission)

        return cls(comment, author, subreddit, post)

    @property
    def text(self):
        return self.comment.body

    @property
    def url(self):
        return f"https://www.reddit.com{self.comment.permalink}"

    @property
    def score(self):
        return self.comment.score

    @property
    def reply_count(self):
        return len(self.comment.replies)
