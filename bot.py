# LECON
# guild sert a prendre les donnée sur serveur
# ctx sert a avoir le contexte
# f sert a faire foncionner tout ce quil ya dans les {}
# les {} sert un introduire autre chose que tu texte (variable) dans une chaine de caractere
# len est comme un ParInt en js il sert a transformer une chaine de caractere en nombre
# \n sert a faire un retour a la ligne comme la balise <br>
# * avant un argument sert a dire qu'il y en auras plusieur mais nous ne connaissons pas le nombre
# mais du coup il est imposible de mettre un nouveau argument a la suite
# .join est une fonction par python qui permet de mettre ce qu'on veut entre chaque mot et on l'ecrit comme sa
# (" ".join(le nom de l'argument))
# FOR IN sert a parcourir une liste for = comme en js (la valeur de depart) et in l'endroit a parcourir
# Pour les EMBED c'est simple il sufit d'ajouter 'discord.Embed' a une variable avec un 'title'(le titre), 'description', un lien 'url' et une couleur avec color = (couleur en exadesimal)
# on peut aussi lui ajouter a cette embed une image avec la commande '(nom de la variable).set_thumbnail(url = (l'url de l'image)
# Pour ajouter du contenue a l'embed on utilise (nom de la variable).add_field a qui on peut mettre plein de parametre tel que 'name' 'value'
# Pour les embed on peut y ajouter un auteur et sa pp avec la commande (nom de la variable).set author(name = ctx.author.name(pour son nom) et icon_url = ctx.author.avatar.url(pour sa pp))
# comme le math random en js il exciste un equivalant pour choisir aleatoirement un item qu'on a crée dans un tableau (comme un js) au prealable avec la commande (text = 'random.choise(nom de votre tableau))

import os
import asyncio
import discord
# import youtube_dl
from discord.ext import commands
import random

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('Token')
default_intents = discord.Intents.default()
default_intents.members = True
new = discord.Client(intents=default_intents)
client = commands.Bot(command_prefix="+")


@client.event
async def on_ready():
    print("Le bot est prêt")
    await client.change_presence(activity=discord.Activity
    (type=discord.ActivityType.watching, name="En developpement"))


 # COMMANDES CLASSIQUE


@client.command()
@commands.has_permissions(administrator=True)
async def latence(ctx):
    embed = discord.Embed(title = "**Latence**")
    embed.set_thumbnail(url ="https://images.frandroid.com/wp-content/uploads/2021/03/latence-reseau-lag.png")
    embed.add_field(name="Latence tu bot",value=f"**{client.latency}**")
    await ctx.send (embed = embed)
    await ctx.message.delete()

@client.command()
async def say(ctx, *texte):
    await ctx.send(" ".join(texte))
    await ctx.message.delete()
    print(f"{ctx.message.author} cette utilisateur a utiliser la commande say pour ecrire {texte}")


# BIENVENUE


# @new.event
# async def on_member_join(member):
#     discu: discord.TextChannel = new.get_channel(898616512749912067)
#     pseudo = member.mention
#     await discu.send(content=f"Bienvenue sur Zanimaux {pseudo}", delete_after=30)


@client.command()
async def n(ctx, new_member: discord.Member):
    server = ctx.guild
    pseudo = new_member.mention
    await ctx.send(content=f"**Bienvenue a toi {pseudo} sur {server.name} ! \n Profite bien de ton sejour ici :)**",
                   delete_after=30)
    await ctx.message.delete()

    # COMMANDE DE MUTE/UNMUTE


async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name="Mute",
                                            permissions=discord.Permissions(
                                                send_messages=False,
                                                speak=False),
                                            reason="Creation du role Mute")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages=False, speak=False)
    return mutedRole


async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Mute":
            return role

    return await createMutedRole(ctx)


@client.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, *, reason="Aucune raison n'a etais saisi"):
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"{member.mention} a été mute !", delete_after=3)


@client.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member, *, reason="Aucune raison n'a etais saisi"):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason=reason)
    await ctx.send(f"{member.mention} a été unmute !")


# COMMANDE DE BAN/UNBAN/KICK


@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.ban(user, reason=reason)
    await ctx.send(f"{user} à été ban \n Pour raison :{reason}")


@commands.has_permissions(administrator=True)
async def unban(ctx, user):
    userName, userId = user.split("#")
    bannedUsers = await ctx.guild.bans()
    for i in bannedUsers:
        if i.user.name == userName and i.user.discriminator == userId:
            await ctx.guild.unban(i.user)
            await ctx.send(f"{user} à été unban")
            return
        await ctx.send("L'utilisateur que vous cherchez a unban n'a pas été trouvé")


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.User, *reason):
    reason = " ".join(reason)
    await ctx.guild.kick(user, reason=reason)
    await ctx.send(f"{user} à été kick \n Pour raison :{reason}")


# BAN LIST


# @client.command()
# @commands.has_permissions(administrator=True)
# async def banlist(ctx):
#     bannedUsers = await ctx.guild.bans()
#     for i in bannedUsers:


# COMMANDE PERSONALISÉ POUR RUNA


def commandeRuna(ctx):
    return ctx.message.author.id == 529254405271453707


@client.command()
@commands.check(commandeRuna)
async def madeinheaven(ctx, heaven: discord.Member):
    pseudo = heaven.mention
    await ctx.send(f"**- Le sort a été jeté sur {pseudo}**")
    await asyncio.sleep(4)
    await ctx.send("**- L'Univers se dilate....**")
    await asyncio.sleep(4)
    await ctx.send("**- Tu n'en fais plus parti**")
    await asyncio.sleep(4)
    await ctx.send("**- L'univers ne veut plus de toi**")
    await asyncio.sleep(4)
    # await ctx.guild.ban(heaven)
    await ctx.send("**MADE IN HEAVEN !**")
    await ctx.send("https://tenor.com/view/made-in-heaven-jojo-stand-gif-19197510")
    await ctx.message.delete()


# COMMANDE PERSONALISÉ POUR COOKIE


@client.command()
async def cookie(ctx):
    auteur = ctx.message.author
    await ctx.send(f"Tien voila ton cookie {auteur.mention} :3", delete_after=10)
    await asyncio.sleep(1)
    await ctx.send("https://emoji.gg/assets/emoji/4809-minecraft-cookie.png", delete_after=9)
    await ctx.message.delete()


# COMMANDE PERSONALISÉ POUR DONNER UN COOKIE


@client.command()
async def givecookie(ctx, drop: discord.Member):
    auteur = ctx.message.author
    await ctx.send(f"Tien {drop.mention} ce cookie vien de t'être offer de la par de {auteur.mention} :3")
    await asyncio.sleep(1)
    await ctx.send("https://emoji.gg/assets/emoji/4809-minecraft-cookie.png")
    await ctx.message.delete()



# COMMANDE JAIL

async def createJailRole(ctx):
    jailRole = await ctx.guild.create_role(name="jail",
                                           permissions=discord.Permissions(
                                               view_channel=False, ),
                                           reason="Creation du role jail")
    for channel in ctx.guild.channels:
        await channel.set_permissions(jailRole, view_channel=False)
    return jailRole


async def createMemberRole(ctx):
    memberRole = await ctx.guild.create_role(name="Membre",
                                             permissions=discord.Permissions(
                                                 view_channel=False, ),
                                             reason="Creation du role Membre")
    for channel in ctx.guild.channels:
        await channel.set_permissions(memberRole, view_channel=False)
    return memberRole


async def getJailRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "jail":
            return role

    return await createJailRole(ctx)


async def RemoveMemberRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Membre":
            return role

    return await createMemberRole(ctx)


# IN JAIL


@client.command()
@commands.has_permissions(administrator=True)
async def jail(ctx, member: discord.Member):
    jailRole = await getJailRole(ctx)
    memberRole = await RemoveMemberRole(ctx)
    await member.add_roles(jailRole)
    await member.remove_roles(memberRole)
    await ctx.send(f"{member.mention} est maintenant en prison !")
    await ctx.message.delete()


# UNJAIL


@client.command()
@commands.has_permissions(administrator=True)
async def unjail(ctx, member: discord.Member):
    jailRole = await getJailRole(ctx)
    memberRole = await RemoveMemberRole(ctx)
    await member.remove_roles(jailRole)
    await member.add_roles(memberRole)
    await ctx.send(f"{member.mention} est sorti de prison !")
    await ctx.message.delete()


@client.event
async def last_message(ctx):
    last_msg = ctx.message.author
    if ctx.last_message == "assistante":
        await ctx.send(f"Vous parlez de moi {last_msg} ?")



# COMMANDE POUR JOUER DE LA MUSIQUE

# musics = {}

# ytdl = youtube_dl.YoutubeDL()


# class Video:
#     def __init__(self, link):
#         video = ytdl.extract_info(link, download = False)
#         video_format = video["formets"][0]
#         self.url = video["webpage_url"]
#         self.stream_url = video_format["url"]


# def play_song(voiceClient,song):
#     source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url , before_options = '-reconnect 1 -reconnected_streamed 1 -reconnect_delay_max 5'))

#     voiceClient.play(source)

# @client.command()
# async def play(ctx, url):
#     print("play")
#     voiceClient = ctx.guild.voice_client

#     if voiceClient and voiceClient.channel:
#         video = Video(url)
#         musics[ctx.guild].append(video)

#     else:
#         channel = ctx.author.voice.channel
#         video = Video(url)
#         musics[ctx.guild] = []
#         voiceClient = await channel.connect()
#         await ctx.send(f"Je lance : {video.url} ")
#         play_song(client, video)



client.run(TOKEN)
