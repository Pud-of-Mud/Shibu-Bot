# Dependances
import discord
import os

from discord import app_commands
from discord.ext import commands
from keep_alive import keep_alive

# Token Varables, etc
GUILD_ID = 771181244427010058
botToken = os.environ['TOKEN']

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


# Slash Commands
@app_commands.command()
async def dontusethiscommand(interaction: discord.Interaction):
  await interaction.response.send_message("Placeholder Text!")

@app_commands.command()
async def uselesscommand(interaction: discord.Interaction):
  await interaction.response.send_message("Placeholder Text!")
  
tree.add_command(dontusethiscommand)
tree.add_command(uselesscommand)

# Events
@client.event
async def on_ready():
  await tree.sync()
  print('We\'re in. We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message): 
  if "nerd" in message.content or "Nerd" in message.content:
    await message.add_reaction("\U0001F913")
  
  if message.content.startswith('!ping'):
    await message.channel.send("@everyone has been pinged!")
  
  # Thumbs up game!
  if message.content.startswith('👍'):
    channel = message.channel
    await channel.send('Send me that 👍 reaction, mate')

    def check(reaction, user):
        return user == message.author and str(reaction.emoji) == '👍'

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await channel.send('👎')
    else:
        await channel.send('👍')
  
  # Profanity filter
  if message.author != client.user:
    if "Kys" in message.content or "kys" in message.content:
      await message.channel.send("thats not very nice :((")
    elif "shit" in message.content or "fuck" in message.content or "bitch" in message.content or "ass" in message.content:
      await message.channel.send("You can't say that, there are children present :\ ")
  
  # PK Fire
  if "pk" in message.content or "Pk" in message.content:
    await message.channel.send(content="pk... FIRE!")
    
keep_alive()

try:
  token = os.getenv("TOKEN") or ""
  if token == "":
    raise Exception("Please add your token")
  client.run(botToken)
  
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
    else:
        raise e  