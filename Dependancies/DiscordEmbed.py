import discord
from os import getcwd
def DiscordEmbed(Town,FileType="png"):
    embed = discord.Embed(colour=discord.Colour.green(),title=F"{Town}",description="EarthMC Towny Archive")
    TownRender = discord.File(F"{str(getcwd())}/Images/TempRender.{FileType}", filename=F"image.{FileType}")
    BotLogo = discord.File(F"{str(getcwd())}/Images/towny1k.png", filename="imagethumb.png")
    embed.set_image(url=F"attachment://image.{FileType}")
    embed.set_thumbnail(url="attachment://imagethumb.png")
    embed.set_footer(icon_url="attachment://imagethumb.png", text="Archive updated daily")
    files = ([TownRender, BotLogo])
    return embed, files