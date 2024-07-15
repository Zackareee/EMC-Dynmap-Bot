import json
from discord.ext import commands, tasks
from PIL import Image, ImageDraw
import numpy as np
import traceback
from Dependancies.Min3D import *
from Dependancies.Max3D import *
from Dependancies.ImageHandling import *
from Dependancies.Download import *
from Dependancies.DiscordEmbed import *
from Dependancies.DateList import *
TOKEN = 'DISCORD BOT TOKEN GOES HERE'

intents = discord.Intents.default()
intents.message_content = True  # Enable the message_content intent

# Create the client instance with the specified intents
client = commands.Bot(intents=intents, command_prefix='.', help_command=None,
                      description=None, case_insensitive=True)

#to support running on windows or linux systems
if os.name == 'nt':
    s = "#"
else:
    s = "-"

def TownOutline(TownName, Date, Mode=0, Server="Towny"):
    outputx = []
    outputz = []
    outputcolor = []
    outputstring = []
    if path.isfile(F'{str(getcwd())}/JSON/{Server}/{Date}/{Date}.json'):
        with open(F'{str(getcwd())}/JSON/{Server}/{Date}/{Date}.json') as f:
            data = json.load(f)
            for Town in TownName:
                for item in data['sets']['townyPlugin.markerset']['areas']:
                    if Mode == 0:
                        if data['sets']['townyPlugin.markerset']['areas'][item]['label'] == Town and "Shop" not in str(item):
                            outputx.append(
                                [int(x) for x in data["sets"]["townyPlugin.markerset"]["areas"][F"{item}"]["x"]])
                            outputz.append(
                                [int(z) for z in data["sets"]["townyPlugin.markerset"]["areas"][F"{item}"]["z"]])
                            outputcolor.append(
                                data["sets"]["townyPlugin.markerset"]["areas"][F"{item}"]["fillcolor"])
                    else:
                        if data['sets']['townyPlugin.markerset']['areas'][item]['label'].startswith(Town) and "Shop" not in str(item):
                            outputstring.append(
                                data["sets"]["townyPlugin.markerset"]["areas"][F"{item}"]["label"])
        if not Mode == 0:
            return outputstring
        elif len(outputx) == 0 and len(outputz) == 0:
            return None, None, None, None
        else:
            return outputx, outputz, outputcolor, Date
    else:
        return None, None, None, None


def TownRender(TownX, TownZ, Width, Height, text="", FillColor=(0, 255, 255)):
    ImageRender = Image.new('RGB', (Width+17, Height+17), color='white')
    TownOutline = ImageDraw.Draw(ImageRender, 'RGBA')
    ChunkGrid = ImageDraw.Draw(ImageRender)
    Grid(ChunkGrid, Width+17, Height+17)
    for i in range(len(TownX)):
        Tuple = tuple(map(tuple, np.c_[TownX[i], TownZ[i]]))
        TownOutline.polygon(Tuple, outline=(0, 0, 255, 100), fill=(FillColor[i][0], FillColor[i][1], FillColor[i][2], 100)) #drawing the towns
        for j in range(int(len(Tuple))):
            TownOutline.line([Tuple[j-1], Tuple[j]], width=2, fill=(0, 0, 255))
    TownOutline.rectangle([(1, 1), (47, 15)], fill=(255, 255, 255), outline=None, width=1)
    TownOutline.text((4, 4), F"{text}", fill=(0, 0, 0, 128))
    return ImageRender


def TownGif(TownNames, TownDate, Server):
    Gif = []
    GifX = []
    GifZ = []
    Dates = []
    FillColor = '#FFFFFF'
    for i in TownDate:
        TownX, TownZ, FillColor, Date = TownOutline(TownNames, i, Server=Server)
        if TownX == None:
            continue
        else:
            GifX.append(TownX)
            GifZ.append(TownZ)
            Dates.append(Date)
    if FillColor == None:
        FillColor = ['#FFFFFF']
    GifZ = [[[GifZ[j][i][f] - (min3d(GifZ) - 16) for f in range(len(GifZ[j][i]))] for i in range(len(GifZ[j]))] for j in range(len(GifZ))] #gets upper and lower bounds of the towns x and z coordinates over the entire nested array
    GifX = [[[GifX[j][i][f] - (min3d(GifX) - 16) for f in range(len(GifX[j][i]))] for i in range(len(GifX[j]))] for j in range(len(GifX))]
    print(FillColor)
    for i in range(len(GifX)):
        thetuple = [tuple(int(j.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) for j in FillColor]
        Gif.append(TownRender(GifX[i], GifZ[i], max3d(GifX), max3d(GifZ), Dates[i], thetuple))
    return Gif


@client.command(pass_context = True, aliases=['TownRender'])
async def TR(ctx, *args):
  if 571032208429678613 or 571043701938323496 or 632135935563137026 in [y.id for y in ctx.author.roles]: #specific role authentication to only work for staff/moderators
      try:
        TownNames = []
        TownDate = []
        print(TownDate)
        server = "Towny"
        if "aurora" in [x.lower() for x in args]:
          server = "Aurora"
        [TownDate.append(i) if i[0].isnumeric() else TownNames.append(i) for i in args if (i.lower() != "nova" and i.lower() != "aurora")]
        if len(TownDate) == 1:
          TownX, TownZ, FillColor, ThisDate = TownOutline(TownNames,TownDate[0],Server=server)
          if TownX == None:
            await ctx.send("``Invalid Date or Town. Town Names are case sensitive. Check towns with Tsearch``")
          else:
            TownX = [[TownX[j][i] - (min2d(TownX) - 16) for i in range(len(TownX[j]))] for j in range(len(TownX))] #stupid math to get the upper and lower bounds of the towns x and z coordinates to have a border around the image
            TownZ = [[TownZ[j][i] - (min2d(TownZ) - 16) for i in range(len(TownZ[j]))] for j in range(len(TownZ))]
            TownRender(TownX, TownZ, max2d(TownX), max2d(TownZ),TownDate[0],FillColor=[tuple(int(j.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) for j in FillColor]).save(F"{str(getcwd())}/Images/TempRender.png")
            embed, files = DiscordEmbed(TownNames, "png")
            await ctx.send(files=files, embed=embed)
        elif len(TownDate) > 1:
          Gif = TownGif(TownNames,TownDate,server)
          print(Gif)
          if Gif == None:
            await ctx.send("``Invalid Date or Town. Town Names are case sensitive. Check towns with Tsearch``")
          else:
            try:
                Gif[0].save(F"{str(getcwd())}/Images/TempRender.gif",save_all=True, append_images=Gif[1:], optimize=False, duration=1000, loop=0)
            except:
                await ctx.send("``Town Not Found``")
                return
            embed, files = DiscordEmbed(TownNames, "gif")
            await ctx.send(files=files, embed=embed)
      except Exception:
            await ctx.send("```py\n" + traceback.format_exc() + "```")


@client.command(pass_context=True)
async def Gif(ctx, *args):
    if 571032208429678613 or 571043701938323496 or 632135935563137026 in [y.id for y in ctx.author.roles]: #specific role authentication to only work for staff/mods
        try:
            TownNames = []
            TownDate = []
            [TownDate.append(i) if i[0].isnumeric() else TownNames.append(i) for i in args if (i != "nova" and i.lower() != "aurora")]
            server = "Towny"
            if "aurora" in [x.lower() for x in args]:
                server = "Aurora"
            TownDate = [str(d) for d in month_date(datetime.strptime(TownDate[0], '%d.%m.%y').date())]
            Gif = TownGif(TownNames, TownDate, server)
            if Gif == None:
                await ctx.send("``Invalid Date or Town. Town Names are case sensitive. Check towns with Tsearch``")
            else:
                try:
                    Gif[0].save(F"{str(getcwd())}/Images/TempRender.gif", save_all=True, append_images=Gif[1:],optimize=False, duration=1000, loop=0)
                except:
                    await ctx.send("``Town or Date Not Found``")
                    return
                embed, files = DiscordEmbed(TownNames, "gif")
                await ctx.send(files=files, embed=embed)
        except Exception:
            await ctx.send("```py\n" + traceback.format_exc() + "```")

@client.command(pass_context=True, aliases=['Search', 'TSearch'])
async def TS(ctx, *args):
    if 571032208429678613 or 571043701938323496 or 632135935563137026 in [y.id for y in ctx.author.roles]:
        TownNames = []
        TownDate = []
        [TownDate.append(i) if i[0].isnumeric() else TownNames.append(i) for i in args if (i != "nova" and i.lower() != "aurora")]
        server = "Towny"
        if "aurora" in [x.lower() for x in args]:
            server = "Aurora"
        if len(TownDate) == 1:
            Towns = TownOutline(TownNames, TownDate[0], 1, server)
            await ctx.send(sorted(Towns))

#downloads json files if they dont exist
@tasks.loop(hours=1)
async def HourCounter():
    if MarkerDownload("Towny"):
        channel = client.get_channel(719903775556370495)
        file = discord.File(F"{str(getcwd())}/JSON/Towny/{str(datetime.today().strftime(f'%{s}d.%{s}m.%y'))}/{str(datetime.today().strftime(f'%{s}d.%{s}m.%y'))}.json",
                            filename=F"Towny_{str(datetime.today().strftime(f'%{s}d.%{s}m.%y'))}.json")
        await channel.send(file=file)
    if MarkerDownload("Aurora"):
        channel = client.get_channel(719903775556370495)
        file = discord.File(F"{str(getcwd())}/JSON/Aurora/{str(datetime.today().strftime(f'%{s}d.%{s}m.%y'))}/{str(datetime.today().strftime(f'%{s}d.%{s}m.%y'))}.json",
                            filename=F"Aurora_{str(datetime.today().strftime(f'%{s}d.%{s}m.%y'))}.json")
        await channel.send(file=file)


@client.event
async def on_ready():
    print('Bootup Complete')
    HourCounter.start()

@client.command()
async def shutdown(ctx, *args):
    if 571032208429678613 in [y.id for y in ctx.author.roles] or 571043701938323496 in [y.id for y in ctx.author.roles]:
        await ctx.bot.logout()

try:
    client.run(TOKEN)
except RuntimeError:
    print('[Shutdown]')
    quit()
