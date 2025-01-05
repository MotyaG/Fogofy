import disnake
from disnake import TextInputStyle
from disnake.ext import commands
import os

intents = disnake.Intents.all()


def getBot():
    bot = commands.Bot(command_prefix="f.", intents=intents)
    return bot


bot = getBot()


def getChannel(channel):
    embChannel = bot.get_channel(channel.id)
    return embChannel


@bot.event
async def on_ready():
    print("Fogofy started!")


for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        bot.load_extension(f"cogs.{file[:-3]}")

bot.run("")
