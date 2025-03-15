# Contains the main bot logic
import discord
from config.config import DISCORD_TOKEN  # Fetch APIs
from src.discord_manager import DiscordBot  # Import the DiscordBot Class

# Initialize Discord client
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent

bot = DiscordBot(intents=intents)

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)  # Run the bot with the token
