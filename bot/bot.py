# bot.py
import discord
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()  # Load environment variables from .env file
TOKEN = os.getenv('DISCORD_TOKEN')

# Define the intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    # Prevent bot from responding to its own messages
    if message.author == client.user:
        return

    # Respond to the test command in any channel
    if message.content == '!test':
        response = 'Test command received!'
        await message.channel.send(response)

    # Extended "prob" command functionality
    if message.content.startswith('!prob'):
        if isinstance(message.channel, discord.DMChannel):
            # Extract the number from the message
            try:
                _, num_str = message.content.split(' ', 1)
                num = int(num_str)  # Convert to integer
                if 0 <= num <= 100:
                    # Get current day in UTC
                    current_day = datetime.utcnow().strftime('%Y-%m-%d')
                    print(f'Current Day: {current_day}, Value: {num}, Username: {message.author.name}')
                    await message.author.send(f'Value received: {num}')
                else:
                    await message.author.send('Please send a number between 0 and 100.')
            except ValueError:
                await message.author.send('Please send a valid number.')
            except Exception as e:
                await message.author.send(
                    'Error processing your command. Make sure it is in the format `!prob number`.')
        else:
            await message.channel.send("Please send me this command in a private message.")


client.run(TOKEN)
