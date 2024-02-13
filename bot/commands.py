# commands.py
from discord_bot import BotCommand
import discord
import re
from datetime import datetime, timedelta
import asyncio
import os

# Assuming stream_info is a global variable
stream_info = {'url': None, 'timestamp': None}

async def test_command(bot, message):
    await message.channel.send('Test command received!')

async def shrek_command(bot, message):
    image_path = 'bot/static/shrek-rizz.png'
    with open(image_path, 'rb') as image:
        discord_file = discord.File(image, filename='shrek-rizz.png')
        await message.channel.send(file=discord_file)

# You can define other commands here following the same pattern.
async def reset_stream_info():
    await asyncio.sleep(4 * 3600)  # Wait for 4 hours
    stream_info['url'] = None
    stream_info['timestamp'] = None
    print('Stream info has been reset.')

async def setstream_command(bot, message):
    if isinstance(message.channel, discord.DMChannel):
        _, url = message.content.split(' ', 1)
        # Validate the YouTube URL
        if re.match(r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$', url):
            stream_info['url'] = url
            stream_info['timestamp'] = datetime.utcnow()
            await message.author.send(f'Stream URL set: {url}')
            # Print an announcement in the general chat
            general_channel = bot.client.get_channel(int(os.getenv('GENERAL_CHANNEL_ID')))
            await general_channel.send(f'@everyone A new stream has started! {url}')
            # Reset the stream info after 4 hours
            bot.client.loop.create_task(reset_stream_info())
        else:
            await message.author.send("Invalid YouTube URL. Please make sure you're sending a valid YouTube stream URL.")