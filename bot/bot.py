# bot.py
from discord_bot import DiscordBot, BotCommand
from commands import test_command, shrek_command, setstream_command, stream_command, prob_command
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
TOKEN = os.getenv('DISCORD_TOKEN')
GENERAL_CHANNEL_ID=os.getenv('GENERAL_CHANNEL_ID')

if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    discord_bot = DiscordBot(TOKEN)

    # Register commands
    discord_bot.add_command(BotCommand('!test', 'Reply with "Test command received!"', test_command))
    discord_bot.add_command(BotCommand('!shrek', 'Post a Shrek picture.', shrek_command))
    discord_bot.add_command(BotCommand('!setstream', 'Set the stream URL (DM only). Announces the stream in the general channel.', setstream_command))
    discord_bot.add_command(BotCommand('!stream', 'Display the current stream URL if available.', stream_command))
    discord_bot.add_command(BotCommand('!prob', 'Set or view the probability of a "lolnight" happening.', prob_command))


    # Start the bot
    discord_bot.run()
