# discord_bot.py
import discord

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

        @self.client.event
        async def on_ready():
            print(f'{self.client.user} has connected to Discord!')

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
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
