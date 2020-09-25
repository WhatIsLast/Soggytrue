from discord.ext import commands, tasks
from discord.utils import get
import discord
import random
from itertools import cycle
import json
import os
import sys, traceback


def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


client = commands.Bot(command_prefix=get_prefix)

status = cycle(['I am Human', 'I see you'])


@client.event
async def on_ready():
    change_status.start()
    print(f'{client.user} is ready!')


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game(next(status)))


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '-'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop[str(guild.id)]

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.command()
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    await ctx.send(f'Prefix changed to {prefix}')


@client.command(pass_context=True)
@commands.has_role('Best Boy')
async def addrole(ctx, role: discord.Role, user: discord.Member):
    await user.add_roles(role)
    await ctx.send(f'Successfully given {role.mention} to {user.mention}')


@client.command(pass_context=True)
@commands.has_role('Best Boy')
async def removerole(ctx, role: discord.Role, user: discord.Member):
    await user.remove_roles(role)
    await ctx.send(f'Successfully removed {role.mention} from {user.mention}')


@commands.command()
async def short(ctx):
    Jack = get(ctx.guild.members, name='shawhan.jack')
    await ctx.send(f'Jack is short:\n{Jack.mention}')


@client.command(name='8ball')
async def _8ball(ctx, *, question):
    responses = ['Yes', 'No', 'Dumb Question', 'Interesting Question']
    await ctx.send(f'Question: {question}\nAnswer:{random.choice(responses)}')


@client.command()
async def coin_flip(ctx):
    result = ['Heads', 'Tails']
    await ctx.send(f'Result: {random.choice(result)}')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid Command Used")


@changeprefix.error
async def changeprefix_error(ctx, error):
    await ctx.send("Please add a prefix")


initial_extensions = ['cogs.mods']

if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)

client.run('NzU4NDE3NzY5ODg3Njk0OTQw.X2uplw.r6vsk6jdbOT8IZ6y3OJUY4OGegc')
