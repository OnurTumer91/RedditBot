# Contains the main bot logic
import discord
import threading  # For prometheus metrics
from prometheus_client import start_http_server, Counter
from config.config import DISCORD_TOKEN  # Fetch APIs
from src.discord_manager import DiscordBot  # Import the DiscordBot Class

# Initialize Discord client
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent

bot = DiscordBot(intents=intents)

#  Prometheus
messages_received = Counter("discord_messages_received", "Number of messages received")
commands_used = Counter("discord_commands_used", "Number of times commands are used")


# Start Prometheus HTTP server on port 8000 (Alt HTTP port)
# Prometheus will scrape metrics from this server
def start_metrics_server():
    start_http_server(8000)


threading.Thread(
    target=start_metrics_server, daemon=True
).start()  # Start the server in a separate thread


# Override event listener to track message metrics
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    messages_received.inc()  # Count received messages

    if message.content.startswith("!reddit"):
        commands_used.inc()  # Count times !reddit is used

    await bot.process_commands(message)  # Keep processing other commands


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)  # Run the bot with the token
