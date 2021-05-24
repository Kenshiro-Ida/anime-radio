import discord
from requests import get
import asyncio
from discord.utils import get
from discord.ext import commands
from youtube_dl import YoutubeDL

client = commands.Bot(command_prefix='f!')

players = {}


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle)
    print('Bot Online.')

    while True:
        await client.change_presence(activity=discord.Game("Anime Lo-Fi Music"))
        await asyncio.sleep(20)
        await client.change_presence(activity=discord.Game("Add me to your server plzzz"))
        await asyncio.sleep(20)
        await client.change_presence(activity=discord.Game(f"f!help"))
        await asyncio.sleep(20)
        await client.change_presence(activity=discord.Game("f!invite"))
        await asyncio.sleep(20)


@client.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    channel = ctx.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        await channel.connect()

    await ctx.send(f"Joined {channel}")


@client.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel")


@client.command(pass_context=True, brief="This will play a song 'play [url]'", aliases=['pl'])
async def play_radio(ctx, url='https://www.youtube.com/watch?v=UoMbwCoJTYM'):
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': 'True'}

    voice = get(client.voice_clients, guild=ctx.guild)
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        I_URL = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(I_URL, **FFMPEG_OPTIONS)
        voice.play(source)
        voice.is_playing()


@client.command(pass_context=True, name='setup', help='Is used to Setup bot in the server')
async def setup(ctx):
    abcde = embed = discord.Embed(
        title="Anime Radio Setup",
        description="Guide to setup bot in your server",
        color=0x3875d6)
    embed.set_thumbnail(url="https://imgur.com/a/I3UPX8n")
    embed.add_field(name="First",
                    value="Make a Stage Channel", inline=False)
    embed.add_field(name="Second",
                    value="Name it whatever you want, I suggest 24/7 Anime Lo-fi Radio", inline=True)
    embed.add_field(name="Third",
                    value="Make the bot join the stage channel using 'f!join' command", inline=True)
    embed.add_field(name="Fourth",
                    value="Invite the bot to the stage by right clicking the bot and selecting invite to speak",
                    inline=True)
    embed.add_field(name="Fifth",
                    value="Type 'f!play_radio' command in any text channel", inline=True)
    embed.set_footer(
        text="Setup Successful...!!!!!!!! It would help me if you invite the bot to your server using 'f!invite'"
             "Created by Kenshiro#2169")
    channel = ctx.message.channel
    await channel.send(embed=abcde)


@client.command(name='invite', help='Get an invite of the bot')
async def invite(ctx):
    embed = discord.Embed(
        title="Anime Radio Bot",
        description="Invite For bot",
        color=discord.Colour.blue())
    embed.add_field(name='If you wish to add me in your server,',
                    value='[Click here to add]( https://discord.com/api/oauth2/authorize?client_id=845348677635145728'
                          '&permissions=2184185600&scope=bot '
                          '&permissions=8&scope=bot )',
                    inline=False)
    channel = ctx.message.channel
    await channel.send(embed=embed)


client.run("ODQ1MzQ4Njc3NjM1MTQ1NzI4.YKfqTg.uMZWGAOcbJB4h6bQowvznEq6EAg")
