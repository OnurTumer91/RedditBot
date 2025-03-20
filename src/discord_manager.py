import discord
from src.reddit_manager import fetch_top_post
from prometheus_client import Counter

#  Prometheus Metrics
messages_received = Counter("discord_messages_received", "Number of messages received")
commands_used = Counter("discord_commands_used", "Number of times commands are used")


class DiscordBot(discord.Client):
    async def on_ready(self):
        print(f"✅ Logged in as {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return  # Ignore bot messages

        messages_received.inc()  # Track total messages received

        if message.content.startswith("!reddit"):
            # Command format: !reddit [sort_method] [subreddit] f.eg !Reddit top technology

            commands_used.inc()  # Track `!reddit` command usage

            parts = message.content.split(" ", 2)
            if len(parts) == 3:
                sort_method = parts[1].lower()  # "top", "new", etc.
                subreddit = parts[2]  # technology, memes, videos etc
            else:
                sort_method = "hot"  # default
                subreddit = parts[1] if len(parts) > 1 else "technology"  # default

            await message.channel.send(
                f"Fetching {sort_method} post from r/{subreddit}..."
            )

            try:
                post = fetch_top_post(subreddit, sort=sort_method)
                title = post["title"]
                url = post["url"]
                score = post["score"]
                image_url = post["image_url"]
                is_video = post["is_video"]
                video_url = post["video_url"]
                selftext = post.get("selftext", "")
                top_comment = post.get("top_comment", "")

                # Build a description that includes the upvote count, selftext, and top comment if available.
                description = f"Upvotes: {score}"
                if selftext:
                    description += f"\n\n{selftext}"
                if top_comment:
                    description += f"\n\n**Top Comment:**\n{top_comment}"

                # Create an embed with the Reddit post details.
                embed = discord.Embed(
                    title=title,
                    url=url,
                    description=f"Top post from r/{subreddit} ({sort_method})\n{description}",
                    color=0x0000FF,  # Blue color
                )

                # For non-GIF images, use thumbnail; for GIFs, we'll send separately.
                if image_url and not image_url.lower().endswith(".gif"):
                    embed.set_thumbnail(url=image_url)

                # Send the embed.
                await message.channel.send(embed=embed)

                # For GIFs, send the URL separately so Discord can render the animated preview.
                if image_url and image_url.lower().endswith(".gif"):
                    await message.channel.send(image_url)

                # Hybrid handling for video:
                # If the post URL is a YouTube link, send it to trigger the native YouTube preview.
                if "youtube.com" in url or "youtu.be" in url:
                    await message.channel.send(url)
                # Otherwise, if it's a Reddit-hosted video, send its video URL.
                elif is_video and video_url:
                    await message.channel.send(video_url)
            except Exception as e:
                await message.channel.send(f"❌ Error: {str(e)}")
