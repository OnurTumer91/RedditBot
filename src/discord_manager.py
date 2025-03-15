import discord
from src.reddit_manager import fetch_top_post


class DiscordBot(discord.Client):
    async def on_ready(self):  # Runs when the bot starts
        print(f"✅ Logged in as {self.user}")

    async def on_message(self, message):  # Listens for messages (!reddit)
        if message.author == self.user:
            return

        if message.content.startswith("!reddit"):
            subreddit = (
                message.content.split(" ", 1)[1]
                if len(message.content.split()) > 1
                else "technology"
            )

            await message.channel.send(f"Fetching top post from r/{subreddit}...")

            try:
                post_title, post_url = fetch_top_post(
                    subreddit
                )  # Fetch top post from Reddit
                response = f"**{post_title}**\n{post_url}"

            except Exception as e:
                response = f"❌ Error: {str(e)}"

            await message.channel.send(response)
