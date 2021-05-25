import discord
from discord.ext import commands
import asyncio


intents = discord.Intents.all()
bot = commands.Bot(command_prefix = "!" , intents = intents) #or any other prefix
bot.remove_command("help")

roles_list = ["Role 1","Role 2"] #list of role names you want to give to people upon using commands. Note : case sensitive!
work_channel = 123456789123456789 #channel id in which you want the bot to work

@bot.event
async def on_ready():
    print("The Bot is ready!")

@bot.event
async def on_message(msg):
    channel_use = bot.get_channel(work_channel)
    if msg.channel != channel_use:
        return
    elif msg.channel == channel_use:
        if msg.content.startswith("!add"):
            await bot.process_commands(msg)
            return
        elif msg.content.startswith("**:x:") or msg.content.startswith("Role not found") or msg.content.startswith("You didn't mention a role") or msg.content.startswith("**Still on cooldown**") or msg.content.startswith(":x:") or msg.content.startswith("**Beginner") or msg.content.startswith("**Intermediate") or msg.content.startswith("**Advanced") or msg.content.startswith("**Fluent") or msg.content.startswith("**Native English"):
            return
        else:
            await msg.delete()

@bot.command()
@commands.cooldown(1,30,commands.BucketType.user)
async def add(ctx,rolename : str = None):
    if rolename == None:
        message_sent3 = await ctx.send("You didn't mention a role name!")
        message_use3 = await ctx.channel.fetch_message(message_sent3.id)
        await asyncio.sleep(10)
        await ctx.message.delete()
        await message_use3.delete()
    else:
        role = discord.utils.get(ctx.guild.roles,name = f"{rolename}")
        if role == None:
            message_sent2 = await ctx.send("Role not found!")
            message_use2 = await ctx.channel.fetch_message(message_sent2.id)
            await asyncio.sleep(10)
            await ctx.message.delete()
            await message_use2.delete()
        else:
            temp_author_roles = ctx.author.roles
            for roles in ctx.author.roles:
                i = 0
                if roles.name in roles_list:
                    if roles.name == rolename:
                        message_sent5 = await ctx.send(":x: You already have this role!")
                        message_use5 = await ctx.channel.fetch_message(message_sent5.id)
                        await asyncio.sleep(10)
                        await ctx.message.delete()
                        await message_use5.delete()
                        break
                    else:
                        await ctx.author.remove_roles(roles)
                        await ctx.author.add_roles(role)
                        message_sent = await ctx.send(f"**{rolename} has been added to {ctx.author.mention}**")
                        await asyncio.sleep(10)
                        await ctx.message.delete()
                        message_use = await ctx.channel.fetch_message(message_sent.id)
                        await message_use.delete()
                        break
                elif roles.name not in roles_list:
                    del temp_author_roles[i]
                    if len(temp_author_roles) == 0:
                        await ctx.author.add_roles(role)
                        message_sent4 = await ctx.send(f"**{rolename} has been added to {ctx.author.mention}**")
                        await asyncio.sleep(10)
                        await ctx.message.delete()
                        message_use4 = await ctx.channel.fetch_message(message_sent4.id)
                        await message_use4.delete()
                        return
                    else:
                        i = i + 1
                        continue
                else:
                    return
                   
@add.error
async def add_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        em = discord.Embed(description = "**:x: Bot missing Permissions**", colour = discord.Colour.red())
        await ctx.send(embed = em)
    elif isinstance(error, commands.CommandOnCooldown):
        message_sent = await ctx.send("**Still on cooldown**, please try again in {:.2f}s".format(error.retry_after))
        message_use = await ctx.channel.fetch_message(message_sent.id)
        await asyncio.sleep(10)
        await ctx.message.delete()
        await message_use.delete()

bot.run("bot token")
