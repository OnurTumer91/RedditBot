# Contains the main bot logic
import discord
import threading  # For Prometheus metrics
from prometheus_client import start_http_server  # Only keeping what's necessary
from config.config import DISCORD_TOKEN  # Fetch APIs
from src.discord_manager import DiscordBot  # Import the DiscordBot Class

# Initialize Discord client
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent

bot = DiscordBot(intents=intents)  # Use the class from discord_manager.py


# Start Prometheus HTTP server on port 8000
# Prometheus will scrape metrics from this server
def start_metrics_server():
    start_http_server(8000)


# Start the Prometheus server in a separate thread to avoid blocking the bot
threading.Thread(target=start_metrics_server, daemon=True).start()


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)  # Run the bot with the token
