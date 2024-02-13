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
            bot.stream_info['url'] = url
            bot.stream_info['timestamp'] = datetime.utcnow()
            await message.author.send(f'Stream URL set: {url}')
            # Print an announcement in the general chat
            general_channel = bot.client.get_channel(int(os.getenv('GENERAL_CHANNEL_ID')))
            await general_channel.send(f'@everyone A new stream has started! {url}')
            # Reset the stream info after 4 hours using the bot's method
            bot.client.loop.create_task(bot.reset_stream_info())
        else:
            await message.author.send("Invalid YouTube URL. Please make sure you're sending a valid YouTube stream URL.")


async def stream_command(bot, message):
    stream_info = bot.stream_info
    if stream_info['url'] and stream_info['timestamp']:
        # Check if the stream URL is still valid (not older than 4 hours)
        if datetime.utcnow() - stream_info['timestamp'] < timedelta(hours=4):
            await message.channel.send(f'Current stream URL: {stream_info["url"]}')
        else:
            await message.channel.send('There is no active stream at the moment.')
    else:
        await message.channel.send('There is no active stream at the moment.')


async def prob_command(bot, message):
    parts = message.content.split(' ')
    command = parts[0]
    additional_text = len(parts) > 1

    if not additional_text:
        # Show probabilities
        response = bot.get_lolnight_prob()
        await message.channel.send(response)
    elif additional_text and isinstance(message.channel, discord.DMChannel):
        try:
            num = int(parts[1])
            if 0 <= num <= 100:
                current_day = datetime.utcnow().strftime('%Y-%m-%d')
                if current_day not in bot.lolnight_prob:
                    bot.lolnight_prob[current_day] = {}
                bot.lolnight_prob[current_day][message.author.name] = num
                await message.author.send(f'Your probability for a lolnight happening today is set to {num}%.')
            else:
                await message.author.send('Please send a number between 0 and 100.')
        except ValueError:
            await message.author.send('Please send a valid number.')
    else:
        # Inform about proper usage in public channels
        await message.channel.send('To set your probability for a "lolnight" happening, please send `!prob [number]` in a direct message. Use `!prob` in this channel without additional text to view today\'s probabilities.')