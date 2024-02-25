# bot.py
from discord_bot import DiscordBot, BotCommand
from commands import test_command, shrek_command, setstream_command, stream_command, prob_command, fetchstats_command, ask_command
import os
from dotenv import load_dotenv
from db import init_db

load_dotenv()  # Load environment variables from .env file
TOKEN = os.getenv('DISCORD_TOKEN')
GENERAL_CHANNEL_ID=os.getenv('GENERAL_CHANNEL_ID')

if __name__ == "__main__":
    init_db()
    discord_bot = DiscordBot(TOKEN)

    # Register commands
    discord_bot.add_command(BotCommand('!test', 'Reply with "Test command received!"', test_command))
    discord_bot.add_command(BotCommand('!shrek', 'Post a Shrek picture.', shrek_command))
    discord_bot.add_command(BotCommand('!setstream', 'Set the stream URL (DM only). Announces the stream in the general channel.', setstream_command))
    discord_bot.add_command(BotCommand('!stream', 'Display the current stream URL if available.', stream_command))
    discord_bot.add_command(BotCommand('!prob', 'Set or view the probability of a lolnight happening.', prob_command))
    discord_bot.add_command(BotCommand('!stats', 'Retrieve and refreshes BF2042 stats.', fetchstats_command))
    discord_bot.add_command(BotCommand('!askGPT', 'Ask GPT about your BF2042 stats (~0.50€ per).', ask_command))
    # Start the bot
    discord_bot.run()
