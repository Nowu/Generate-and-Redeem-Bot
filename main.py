from discord.ext import commands
import discord
from time import sleep
import uuid
import os  # import os module

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

yourrole = 'Donator' 

@bot.event
async def on_ready():
    print("Bot is online and ready")

@bot.command()
@commands.has_role('ALLOWED ROLE FOR GENERATING KEYS')  # 
async def gen(ctx, amount):
    key_amt = range(int(amount))
    with open("keys.txt", "a") as f:
        show_key = ''
        for x in key_amt:
            key = str(uuid.uuid4())
            show_key += "\n" + key
            f.write(key + "\n")

        if len(str(show_key)) == 37:
            show_key = show_key.replace('\n', '')
            await ctx.send(f"Key: {show_key}")
            return 0
        if len(str(show_key)) > 37:
            await ctx.send(f"Keys: {show_key}")
        else:
            await ctx.send("Something's wrong")

@bot.command()
async def redeem(ctx, key):
    if len(key) != 36:
        em = discord.Embed(color=0xff0000)
        em.add_field(name="Invalid Key", value="Inputted key has wrong length!")
        await ctx.send(embed=em)
        return 0

    # Check if used keys.txt file exists. If not, create it.
    if not os.path.isfile("used keys.txt"):
        open("used keys.txt", 'w').close()

    with open("used keys.txt") as f:
        if key in f.read():
            em = discord.Embed(color=0xff0000)
            em.add_field(name="Invalid Key", value="Input key has already been used!")
            await ctx.send(embed=em)
            return 0

    with open("keys.txt") as f:
        if key in f.read():
            with open("used keys.txt", "a") as uf:
                uf.write(key + "\n")
            role = discord.utils.get(ctx.guild.roles, name=yourrole)
            await ctx.author.add_roles(role)
            em = discord.Embed(color=0x008525)
            em.add_field(name="Key Redeemed", value="Key has now been redeemed")
            await ctx.send(embed=em)
        else:
            em = discord.Embed(color=0xff0000)
            em.add_field(name="Invalid Key", value="Inputted key is invalid!")
            await ctx.send(embed=em)

@gen.error  # Add an error handler for the gen command
async def gen_error(ctx, error):
    if isinstance(error, commands.CheckFailure):  
        await ctx.send("You do not have the correct role for this command.")

bot.run('bot token here')
