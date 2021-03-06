import discord
import asyncio
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from scripts import help, db
import sqlite3


categories = """

More Information: ``help [Module]``
-----------------------------------
**moderation** - Moderation module
**minigames** - Minigames module
**fun** - Fun Module
**music** - Music Module
**infosystem** - Information module
**system** - Submission and ticket creation information 
**config** - Settings for server setup 
**tools** - Useful tools
**sudo** - Help for bot owners
**Use $invite for bot invite links**
""" 

class helper(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.group(invoke_without_command=True) # Команда Help
    async def help(self, ctx: SlashContext):
        connect = sqlite3.connect(db.main)
        cursor = connect.cursor()
        cursor.execute(db.select_table("prefixes","prefix","guild_id", ctx.guild.id))
        res = cursor.fetchone()
        cursor.close()
        connect.close()
        if res is None:
            res = "$"
        embed = discord.Embed(
            title="Help System",
        )    
        embed.add_field(
            name=":books: **Commands**",
            value=categories,
            inline=False
        )    
        await ctx.send(embed=embed)
    
    @help.command(pass_context=True)
    async def moderation(self, ctx: SlashContext):
        modo = discord.Embed(
            title="Help System",
        )    
        modo.add_field(
            name="**Moderation**",
            value=help.mod,
            inline=False
        )    
        await ctx.send(embed=modo)
    
    @help.command(pass_context=True)
    async def minigames(self, ctx: SlashContext):
        mindo = discord.Embed(
            title="Help System",
        )    
        mindo.add_field(
            name="**Minigames**",
            value=help.minigames,
            inline=False
        )    
        await ctx.send(embed=mindo)
    
    @help.command(pass_context=True)
    async def fun(self, ctx: SlashContext):
        fundo = discord.Embed(
            title="Help System",
        )    
        fundo.add_field(
            name="**Fun**",
            value=help.fun,
            inline=False
        )    
        await ctx.send(embed=fundo)

    @help.command(pass_context=True)
    async def music(self, ctx: SlashContext):
        musdo = discord.Embed(
            title="Help System",
        )    
        musdo.add_field(
            name="**Music**",
            value=help.music,
            inline=False
        ) 
        await ctx.send(embed=musdo)

    @help.command(pass_context=True)
    async def infosystem(self, ctx: SlashContext):
        infodo = discord.Embed(
            title="Help System",
        )    
        infodo.add_field(
            name="**Infosystem**",
            value=help.infosystem,
            inline=False
        )
        await ctx.send(embed=infodo)

    @help.command(pass_context=True)
    async def tools(self, ctx: SlashContext):
        tooldo = discord.Embed(
            title="Help System",
        )    
        tooldo.add_field(
            name="**Tools**",
            value=help.tool,
            inline=False
        )
        await ctx.send(embed=tooldo)

    @help.command(pass_context=True)
    async def system(self, ctx: SlashContext):
        sysdo = discord.Embed(
            title="Help System",
        )    
        sysdo.add_field(
            name="**System**",
            value=help.system,
            inline=False
        )
        await ctx.send(embed=sysdo)

    @help.command(pass_context=True)
    async def sudo(self, ctx: SlashContext):
        sudodo = discord.Embed(
            title="Help System",
        )    
        sudodo.add_field(
            name="**Sudo**",
            value=help.sudo,
            inline=False
        )
        await ctx.send(embed=sudodo)
    
    @help.command(pass_context=True)
    async def config(self, ctx: SlashContext):
        confdo = discord.Embed(
            title="Help System",
        )    
        confdo.add_field(
            name="**Config**",
            value=help.config,
            inline=False
        )
        await ctx.send(embed=confdo)



    @commands.command()
    async def version(self, ctx: SlashContext):
        path = "scripts/version.txt"
        with open(path, "r") as file:
            ver = file.readline()
        vers = discord.Embed(title="Current version", description=ver, color=0xd12ec9)
        await ctx.send(embed=vers)

    @commands.command()
    async def info(self, ctx: SlashContext):
        path = "scripts/version.txt"
        with open(path, "r") as file:
            ver = file.readline()
        embed = discord.Embed(title="Information about bot", description="Listed below", color=0xff6900)
        embed.add_field(name="Current version", value=ver, inline=False)
        embed.add_field(name="Author", value="Bot based on NigamanRPG#6937 KonsoleBot -English translation + additions by Middlle#7488 ", inline=False)
        embed.add_field(name="Thanks", value="NigamanRPG#6937 for konsolebot code on https://computerteam.tk:4600/ , Plastik#5004 for setname command code ", inline=False)
        embed.add_field(name="Hosting", value="Heroku", inline=False)
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)





def setup(bot):
    bot.add_cog(helper(bot))
