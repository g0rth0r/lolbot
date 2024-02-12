# bot.py
import discord
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import asyncio

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

    if message.author == client.user:
        return

    if message.content == '!test':
        await message.channel.send('Test command received!')

    # Handle the !setstream command
    if message.content.startswith('!setstream'):
        if isinstance(message.channel, discord.DMChannel):
            _, url = message.content.split(' ', 1)
            # Here, you would add validation for the URL
            stream_info['url'] = url
            stream_info['timestamp'] = datetime.utcnow()
            await message.author.send(f'Stream URL set: {url}')
            # Print an announcement in the general chat (replace 'general_channel_id' with the actual ID)
            general_channel = client.get_channel(int(GENERAL_CHANNEL_ID))
            await general_channel.send(f'@everyone A new stream has started! {url}')
            # Reset the stream info after 4 hours
            client.loop.create_task(reset_stream_info())
        else:
            await message.channel.send("Please use this command in a private message.")

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


client.run(TOKEN)
