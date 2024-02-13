# bot.py
import discord
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import asyncio
import re
import statistics

load_dotenv()  # Load environment variables from .env file
TOKEN = os.getenv('DISCORD_TOKEN')
GENERAL_CHANNEL_ID=os.getenv('GENERAL_CHANNEL_ID')
# Define the intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

stream_info = {'url': None, 'timestamp': None}
lolnight_prob = {}

def get_lolnight_prob():
    """Generates a message with the probability of a lolnight happening for the current day,
    including individual probabilities and a total probability."""
    current_day = datetime.utcnow().strftime('%Y-%m-%d')
    if current_day in lolnight_prob and lolnight_prob[current_day]:
        user_probs = lolnight_prob[current_day]
        individual_messages = [f'{user}: {prob}%' for user, prob in user_probs.items()]
        # Calculate total probability as the average of individual probabilities
        total_prob = statistics.mean(user_probs.values())
        return (f'The probability of "lolnight" happening today ({current_day}) is {total_prob}%.\n'
                f'Individual probabilities:\n' + '\n'.join(individual_messages))
    else:
        return 'No probabilities set for today.'

async def reset_stream_info():
    await asyncio.sleep(4 * 3600)  # Wait for 4 hours
    stream_info['url'] = None
    stream_info['timestamp'] = None
    print('Stream info has been reset.')


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    global stream_info
    global lolnight_prob

    if message.author == client.user:
        return
    # List of supported commands
    supported_commands = ['!test', '!setstream', '!stream', '!prob', '!info']

    if message.content == '!test':
        await message.channel.send('Test command received!')

    # Split command to check for additional parts
    parts = message.content.split(' ')
    command = parts[0]
    additional_text = len(parts) > 1

    # Handle the !setstream command
    if message.content.startswith('!setstream'):
        if isinstance(message.channel, discord.DMChannel):
            _, url = message.content.split(' ', 1)
            # Validate the YouTube URL
            if re.match(r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$', url):
                stream_info['url'] = url
                stream_info['timestamp'] = datetime.utcnow()
                await message.author.send(f'Stream URL set: {url}')
                # Print an announcement in the general chat (replace 'general_channel_id' with the actual ID)
                general_channel = client.get_channel(int(GENERAL_CHANNEL_ID))
                await general_channel.send(f'@everyone A new stream has started! {url}')
                # Reset the stream info after 4 hours
                client.loop.create_task(reset_stream_info())
            else:
                await message.author.send(
                    "Invalid YouTube URL. Please make sure you're sending a valid YouTube stream URL.")

    # Handle the !stream command
    if message.content == '!stream':
        if stream_info['url'] and stream_info['timestamp']:
            # Check if the stream URL is still valid (not older than 4 hours)
            if datetime.utcnow() - stream_info['timestamp'] < timedelta(hours=4):
                await message.channel.send(f'Current stream URL: {stream_info["url"]}')
            else:
                await message.channel.send('There is no active stream at the moment.')
        else:
            await message.channel.send('There is no active stream at the moment.')

    # Handle the !prob command
    if command == '!prob':
        # For DMs or standalone !prob command in public channels, show probabilities
        if not additional_text:
            response = get_lolnight_prob()
            await message.channel.send(response)
        # For !prob with additional text in public channels, inform about proper usage
        elif additional_text and not isinstance(message.channel, discord.DMChannel):
            await message.channel.send('To set your probability for a "lolnight" happening, please send `!prob [number]` in a direct message. Use `!prob` in this channel without additional text to view today\'s probabilities.')

        # Setting probabilities in DMs
        elif isinstance(message.channel, discord.DMChannel) and additional_text:
            try:
                num = int(parts[1])
                if 0 <= num <= 100:
                    current_day = datetime.utcnow().strftime('%Y-%m-%d')
                    if current_day not in lolnight_prob:
                        lolnight_prob[current_day] = {}
                    lolnight_prob[current_day][message.author.name] = num
                    await message.author.send(f'Your probability for a lolnight happening today is set to {num}%.')
                else:
                    await message.author.send('Please send a number between 0 and 100.')
            except ValueError:
                await message.author.send('Please send a valid number.')

    elif message.content.startswith('!') and command not in supported_commands:
        # List of commands and their descriptions
        commands = {
            '!test': 'Reply with "Test command received!"',
            '!setstream [YouTube URL]': 'Set the stream URL (DM only). Announces the stream in the general channel.',
            '!stream': 'Display the current stream URL if available.',
            '!prob [number]': 'In DM, receive a placeholder for probability calculation. In public, announce the probability of lolnight happening.'
        }
        # Building the response string
        response = "**Supported Commands:**\n"
        for command, description in commands.items():
            response += f"**{command}**: {description}\n"

        await message.channel.send(response)

    # No need to add additional else clauses for each command, as the catch-all handles them.

client.run(TOKEN)
