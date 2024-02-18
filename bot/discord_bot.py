# discord_bot.py
import discord
import asyncio
from datetime import datetime
import statistics
from ai_commands import handle_mention
import sqlite3
import db

class BotCommand:
    def __init__(self, name, description, execute_func):
        self.name = name
        self.description = description
        self.execute = execute_func

class DiscordBot:
    def __init__(self, token):
        self.client = discord.Client(intents=discord.Intents.all())
        self.token = token
        self.commands = {}
        self.stream_info = {'url': None, 'timestamp': None}
        self.lolnight_prob = {}  # Add lolnight_prob attribute


        @self.client.event
        async def on_ready():
            print(f'{self.client.user} has connected to Discord!')

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return

            # Check if the bot is mentioned
            if self.client.user.mentioned_in(message) and message.mentions:
                # Remove the mention of the bot to get the rest of the message
                mention_text = message.content.replace(f'<@!{self.client.user.id}>', '').strip()
                # Call the placeholder function or any specific function you've defined
                await handle_mention(self, message, mention_text)
                return

            command_name = message.content.split(' ')[0]
            if command_name in self.commands:
                await self.commands[command_name].execute(self, message)
            elif message.content.startswith('!'):
                await self.show_commands(message)

    def run(self):
        self.client.run(self.token)

    async def show_commands(self, message):
        response = "**Supported Commands:**\n"
        for name, command in self.commands.items():
            response += f"**{name}**: {command.description}\n"
        await message.channel.send(response)

    def add_command(self, command):
        self.commands[command.name] = command

    async def reset_stream_info(self):
        await asyncio.sleep(4 * 3600)  # Wait for 4 hours
        self.stream_info['url'] = None
        self.stream_info['timestamp'] = None
        print('Stream info has been reset.')

    def get_lolnight_prob(self):
        """Fetches and calculates the probability of a lolnight happening for the current day from the database."""
        current_day = datetime.utcnow().strftime('%Y-%m-%d')
        probs = db.fetch_lolnight_probs(current_day)  # Assuming you have this function in db.py

        if probs:
            individual_messages = [f'{user}: {prob}%' for user, prob in probs]
            total_prob = statistics.mean([prob for _, prob in probs])
            return (f'The probability of "lolnight" happening today ({current_day}) is {total_prob}%.\n'
                    f'Individual probabilities:\n' + '\n'.join(individual_messages))
        else:
            return 'No probabilities set for today.'