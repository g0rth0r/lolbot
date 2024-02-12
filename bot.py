# bot.py
import discord
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
TOKEN = os.getenv('DISCORD_TOKEN')

# Define the intents
intents = discord.Intents.default()
intents.messages = True
intents.members = True
intents.message_content = True

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

    # Respond to the "prob" command via a private message
    if message.content.startswith('!prob'):
        if isinstance(message.channel, discord.DMChannel):
            response = 'Placeholder for probability calculation.'
            await message.author.send(response)
        else:
            await message.channel.send("Please send me this command in a private message.")


client.run(TOKEN)
