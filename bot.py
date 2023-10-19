import discord
from discord.ext import commands
import responses

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="?", intents=intents)


async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


# TODO Funkce pro odeslání zprávy na Discord
async def send_discord_message(message_content):
    channel_id = 1164569392240136215

    # Získání cílového kanálu
    channel = client.get_channel(channel_id)

    if channel is not None:
        await channel.send(message_content)
    else:
        print(f"Kanál s ID {channel_id} nebyl nalezen.")


def run_discord_bot():
    TOKEN = 'MTE2NDU5MTc3NzAyMjQ3NjQzMQ.GwVj2g.vREtc-oH1JuowWj1RP1PBGhldx6ghjkVeZYzKk'

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        if client.user.mentioned_in(message):
            await message.channel.send("https://tenor.com/view/wawa-cat-wawawa-meme-gif-25812133")
        if message.content == 'ječná':
            file = discord.File('images/rasicek.png')
            await message.channel.send(file=file)
        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    client.run(TOKEN)
