# LECON
# guild sert a prendre les donner sur serveur
# ctx sert a avoir le contexte
# sert a faire foncionner tout ce quil ya dans les {}
# les {} sert un introduire autre chose que tu texte (variable) dans une chaine de caractere
# len est comme un ParInt en js il sert a transformer une chaine de caractere en nombre
# \n sert a faire un retour a la ligne comme la balise <br>
# * avant un argument sert a dire qu'il y en auras plusieur mais nous ne connaissons pas le nombre
# mais du coup il est imposible de mettre un nouveau argument a la suite
# .join est une fonction par python qui permet de mettre ce qu'on veut entre chaque mot et on l'ecrit comme sa
# (" ".join(le nom de l'argument))
# FOR IN sert a parcourir une liste for = comme en js (la valeur de depart) et in l'endroit a parcourir

import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
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
    await ctx.send(f"Voila la latance du bot {client.latency}", delete_after=5)
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
#         if i == bannedUser:
#             return i


# COMMANDE PERSONALISÉ POUR FOXY


def commandeFoxy(ctx):
    return ctx.message.author.id == 269563995512504321


@client.command()
@commands.check(commandeFoxy)
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
    await ctx.guild.ban(heaven)
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

    # COMMANDE PERSONALISÉ POUR DONNER UN COOKI


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


client.run(TOKEN)
