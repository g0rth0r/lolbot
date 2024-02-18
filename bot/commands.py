# commands.py
from discord_bot import BotCommand
import discord
import re
from datetime import datetime, timedelta
import asyncio
import os
import sqlite3
import db
import statistics
from mqtt_util import publish_message, MQTT_TOPIC
from format_stats import format_player_stats

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
        try:
            _, url = message.content.split(' ', 1)
            # Validate the YouTube URL
            if re.match(r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$', url):
                timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                # Insert stream info into the database using db utility
                db.insert_stream_info(url, timestamp)
                await message.author.send(f'Stream URL set: {url}')
                # Print an announcement in the general chat
                general_channel_id = int(os.getenv('GENERAL_CHANNEL_ID'))
                general_channel = bot.client.get_channel(general_channel_id)
                if general_channel:  # Check if the channel was found
                    await general_channel.send(f'@everyone A new stream has started! {url}')
                else:
                    print(f"Error: General channel with ID {general_channel_id} not found.")
            else:
                await message.author.send("Invalid YouTube URL. Please make sure you're sending a valid YouTube stream URL.")
        except Exception as e:
            print(f"Error setting stream URL: {e}")
            await message.author.send("Sorry, there was an error processing your request.")
    else:
        await message.channel.send("Use this command in a private message.")

async def stream_command(bot, message):
    try:
        stream_info = db.fetch_latest_stream_info()

        if stream_info:
            url, timestamp_str = stream_info
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
            # Check if the stream URL is still valid (not older than 4 hours)
            if datetime.utcnow() - timestamp < timedelta(hours=4):
                await message.channel.send(f'Current stream URL: {url}')
            else:
                await message.channel.send('There is no active stream at the moment.')
        else:
            await message.channel.send('There is no active stream at the moment.')
    except Exception as e:
        print(f"Error fetching stream information: {e}")
        await message.channel.send("Sorry, there was an error processing your request.")


async def prob_command(bot, message):
    parts = message.content.split(' ')
    additional_text = len(parts) > 1

    if not additional_text:
        # Show probabilities
        current_day = datetime.utcnow().strftime('%Y-%m-%d')
        probs = bot.get_lolnight_prob(current_day)
        if probs:
            individual_messages = [f'{user}: {prob}%' for user, prob in probs]
            total_prob = statistics.mean([prob for _, prob in probs])
            response =  (f'The probability of "lolnight" happening today ({current_day}) is {total_prob}%.\n'
                    f'Individual probabilities:\n' + '\n'.join(individual_messages))
        else:
            response = 'No probabilities set for today.'
        await message.channel.send(response)
    elif additional_text and isinstance(message.channel, discord.DMChannel):
        try:
            num = int(parts[1])
            if 0 <= num <= 100:
                current_day = datetime.utcnow().strftime('%Y-%m-%d')
                db.upsert_lolnight_prob(message.author.name, num, current_day)
                probs = bot.get_lolnight_prob(current_day)
                if probs:
                    total_prob = statistics.mean([prob for _, prob in probs]) / 100
                    publish_message(MQTT_TOPIC, str(total_prob))  # Publish the overall probability
                await message.author.send(f'Your probability for a lolnight happening today is set to {num}%.')
            else:
                await message.author.send('Please send a number between 0 and 100.')
        except ValueError:
            await message.author.send('Please send a valid number.')
    else:
        # Inform about proper usage in public channels
        await message.channel.send('To set your probability for a "lolnight" happening, please send `!prob [number]` in a direct message. Use `!prob` in this channel without additional text to view today\'s probabilities.')


async def fetchstats_command(bot, message):
    discord_username = str(message.author)

    # Fetch player configuration using Discord username
    player_config = db.fetch_player_config_by_discord_username(discord_username)
    if player_config:
        _, bf_username, player_id = player_config
        stats = bot.bf_api.get_player_stats(player_id=player_id)
        if stats:
            db.save_player_stats(player_id, stats)
            # Here you can format the stats as you like before sending them back
            parsed_stats = format_player_stats(stats)
            await message.channel.send(parsed_stats)
        else:
            await message.channel.send("Failed to fetch player stats.")
    else:
        await message.channel.send("You are not configured. Please set up your player configuration first.")