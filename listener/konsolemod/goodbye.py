import discord
import asyncio
from datetime import datetime
import functools
import sqlite3
from scripts import db, help
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
class goodbye(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            #now  = datetime.now()
            #time = now.strftime("%H:%M:%S")
            connect = sqlite3.connect(db.main)
            cursor = connect.cursor()
            cursor.execute(db.select_table("goodbye", "channel_id", "guild_id", member.guild.id))
            chan = cursor.fetchone()
            if chan is None:
                return
            else:
                cursor.execute(db.select_table("goodbye", "text", "guild_id", member.guild.id))
                desc = cursor.fetchone()
                if desc is None: 
                    desc = f"{MEMBER} goodbye "
                gb = discord.Embed(title="User Left The Channel", description=(desc[0]).format(MEMBER=member, MENTION=member.mention), color=0xf4211a)
                #gb.add_field(name="Время", value=time, inline=False)
                gb.set_author(name=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
                gb.set_thumbnail(url=f"{member.avatar_url}")
                channel = self.bot.get_channel(id=int(chan[0]))
            cursor.close()
            connect.close()  
            await channel.send(embed=gb)
        except:
            print(f"The server  {member.guild.id} encountered an unknown error. Perhaps the goodbye channel was removed.")


    @commands.group(invoke_without_command=True)
    async def goodbye(self, ctx: SlashContext):
        await ctx.send(help.goodbye)

    @goodbye.command()
    async def channel(self, ctx: SlashContext, channel: discord.TextChannel=None):
        try:
            author =  ctx.message.author     
            if author.guild_permissions.administrator: 
                connect = sqlite3.connect(db.main)
                cursor = connect.cursor()
                cursor.execute(db.select_table("goodbye", "channel_id", "guild_id", ctx.guild.id))
                result = cursor.fetchone()
                if result is None:
                    val = (ctx.guild.id, channel.id)
                    cursor.execute(db.insert_table("goodbye","guild_id","channel_id"), val)
                else:
                    cursor.execute(db.update_table("goodbye", "channel_id", channel.id, "guild_id", ctx.guild.id))
                connect.commit()
                cursor.close()
                connect.close()
                await ctx.send(f"bot: Set the goodbye channel to  {channel.mention}")
            else:
                await ctx.send("bot: You do not have enough permissions - :You require **Administrator**")
        except:
            await ctx.send("bot: Error")


   
    @goodbye.command()
    async def clear(self, ctx: SlashContext):
        try:
            author =  ctx.message.author
            if author.guild_permissions.administrator:
                connect = sqlite3.connect(db.main)
                cursor = connect.cursor()
                cursor.execute(db.select_table("goodbye", "channel_id", "guild_id", ctx.guild.id))
                result = cursor.fetchone()
                if result is None:
                    await ctx.send("bot: Do not have a table for the goodbye channel - Check Database.")
                else:
                    cursor.execute(db.delete_table("goodbye", "guild_id", ctx.guild.id))
                    await ctx.send("bot: Cleared the table")  
                connect.commit()
                cursor.close()
                connect.close()  
            else:
                await ctx.send("bot: You do not have enough permissions - :You require **Administrator**.")
        except:
            await ctx.send("bot: Error")

    @goodbye.command(pass_context=True)
    async def text(self, ctx: SlashContext,*,content=None):
        try:
            author = ctx.message.author
            if author.guild_permissions.administrator:
                if content is None:
                    return await ctx.send("bot: Please type the text you wish for the goodbye message")
                connect = sqlite3.connect(db.main)
                cursor = connect.cursor()
                cursor.execute(db.select_table("goodbye", "text", "guild_id", ctx.guild.id))
                res = cursor.fetchone()
                if res is None:
                    val = (ctx.guild.id, content)
                    cursor.execute(db.insert_table("goodbye","guild_id","text"), val)
                else:
                    val = (content, ctx.guild.id)
                    cursor.execute("UPDATE goodbye SET text = ? WHERE guild_id = ?", val)      
                connect.commit()
                cursor.close()
                connect.close()
                await ctx.send(f"bot: Set the goodbye message text") 
            else:
                await ctx.send("bot: You do not have enough permissions - :You require **Administrator**.")
        except:
            await ctx.send("bot: Error , argument may be invalid")


def setup(bot):
    bot.add_cog(goodbye(bot))