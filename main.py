from typing import Optional
import discord
import os
from discord import app_commands
from discord.ext import commands
import random
import requests
import json
from colorama import init
from colorama import Fore, Back, Style

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Access the values
TOKEN = config['token']
GUILD_ID = config['guild_id']
LOG_ID = config['log_id']

################################################################################################
# WELCOME TO KITSUNE BOB/BOT!
# This bot is not tailored to be run globally. So there are some things you need to do
MY_GUILD = discord.Object(id=GUILD_ID)  # replace with your guild id
token = TOKEN # PLACEHOLDER

init()


class MyClient(discord.Client):

  def __init__(self, *, intents: discord.Intents):
    super().__init__(intents=intents)
    # A CommandTree is a special type that holds all the application command
    # state required to make it work. This is a separate class because it
    # allows all the extra state to be opt-in.
    # Whenever you want to work with application commands, your tree is used
    # to store and work with them.
    # Note: When using commands.Bot instead of discord.Client, the bot will
    # maintain its own tree instead.
    self.tree = app_commands.CommandTree(self)

  # In this basic example, we just synchronize the app commands to one guild.
  # Instead of specifying a guild to every command, we copy over our global commands instead.
  # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
  async def setup_hook(self):
    # This copies the global commands over to your guild.
    self.tree.copy_global_to(guild=MY_GUILD)
    await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)


@client.event
async def on_ready():
  print(f'Logged in as {client.user} (ID: {client.user.id})')
  print('------')


@client.tree.command(name="hello")
@app_commands.describe(user="The user to greet (optional)")
async def hello(interaction: discord.Interaction, user: discord.Member = None):
    """Says hello!"""
    if user is None:  # No user specified, greet the member who used the command
        await interaction.response.send_message(
            random.choice([
                f"Hey {interaction.user.name}! You look like hammered shit!",
                f"Hi {interaction.user.mention}!", f"greetings {interaction.user.name}"
            ])
        )
    else:  # Greet the specified user
        await interaction.response.send_message(
            random.choice([
                f"Hey {user.name}! You look like hammered shit!",
                f"Hi {user.mention}!", f"greetings {user.name}"
            ])
        )

###
@client.tree.command()
@app_commands.rename(url='url')
@app_commands.describe(url='the site to check. (MAKE SURE HTTPS:// IS ON!))')
async def site_check(interaction: discord.Interaction, url: str):
  """Makes a GET request to the URL and returns status code"""
  shit = requests.get(url)
  if shit.status_code == 200:
    await interaction.response.send_message(url + " is an okay [200]")
  else:
    await interaction.response.send_message(url + " is not an okay " +
                                            shit.status_code)


@client.tree.command()
@app_commands.rename(username='username')
@app_commands.describe(
  username=
  'The username of the neocities site. like arezg.neocities.org, put the "arezg"'
)
async def ncinfo(interaction: discord.Interaction, username: str):
  """Gets info about a neocities site"""
  fuck = requests.get("https://neocities.org/api/info?sitename=" + username)
async def ncinfo(interaction: discord.Interaction, username: str):
  """Gets info about a neocities site"""
  fuck = requests.get("https://neocities.org/api/info?sitename=" + username)
  f = json.loads(fuck.text)
  await interaction.response.send_message(f"""
Username: {f['sitename']}
{f['views']} Views
{f['hits']} Hits
Created at: {f['created_at']}
Last Updated: {f['last_updated']}
""")


@client.tree.command()
async def info(interaction: discord.Interaction):
  """Info on this bot"""
  embed = discord.Embed(
    title='My name is Kitsune Bot, and I stan for Alex Mason.')
  embed.description = f"""
I'm Kitsune Bot, I work for **{interaction.guild.name}**.
I work with slash commands and I despise old prefix commands, I also have interaction apps too!
Some of my core features are `Chatbotting`, `Report To Moderators` and `Loving Alex Mason`. Though there is *alot* more
"""
  await interaction.response.send_message(embed=embed)


@client.tree.command()
@app_commands.describe(
  first_value='The first value you want to add something to',
  second_value='The value you want to add to the first value',
)
async def add(interaction: discord.Interaction, first_value: int,
              second_value: int):
  """Adds two numbers together."""
  await interaction.response.send_message(
    f'{first_value} + {second_value} = {first_value + second_value}')


# The rename decorator allows us to change the display of the parameter on Discord.
# In this example, even though we use `text_to_send` in the code, the client will use `text` instead.
# Note that other decorators will still refer to it as `text_to_send` in the code.
@client.tree.command()
@app_commands.rename(text_to_send='text')
@app_commands.describe(text_to_send='Text to send in the current channel')
async def send(interaction: discord.Interaction, text_to_send: str):
  """Sends the text into the current channel."""
  await interaction.response.send_message("Sent", ephemeral=True)
  await interaction.channel.send(text_to_send)


#@client.tree.command()
#@app_commands.rename(person='person')
#@app_commands.rename(ratio='ratio')
#@app_commands.describe(person='Who?')
#@app_commands.describe(ratio='What?')
#async def meter(interaction: discord.Interaction, person: str, ratio: str):
#  """Ratio Meter"""
#  randomV = random.randint(0, 100)
#  await interaction.channel.send(f"{person} is %{randomV} {ratio}")
#

@client.tree.command()
async def dadjoke(interaction: discord.Interaction):
  """Receive a dad joke to make your day"""
  headerdj = {"Accept": "text/plain"}
  urldj = "https://icanhazdadjoke.com/"
  maindj = requests.get(urldj, headers=headerdj)
  await interaction.response.send_message(maindj.text)


@client.tree.command()
async def link(interaction: discord.Interaction):
  """Gives YOU a link to arezg's Website"""
  if random.randint(1, 5) == 1:
    await interaction.response.send_message("no")
  else:
    await interaction.response.send_message(
      "There you go: https://arezg.neocities.org")


@client.tree.command()
@app_commands.rename(question='question')
@app_commands.describe(question='The question to ask 8ball')
async def eightball(interaction: discord.Interaction, question: str):
  """Ask the magic 8ball a question!"""
  await interaction.response.send_message(f"""
> {question}
🎱🔻 {random.choice(["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes definitely.", "You may rely on it", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later", "Better not tell you now", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."])}
""")


# To make an argument optional, you can either give it a supported default argument
# or you can mark it as Optional from the typing standard library. This example does both.
@client.tree.command()
@app_commands.describe(
  member=
  'The member you want to get the joined date from; defaults to the user who uses the command'
)
async def joined(interaction: discord.Interaction,
                 member: Optional[discord.Member] = None):
  """Says when a member joined."""
  # If no member is explicitly provided then we use the command user here
  member = member or interaction.user

  # The format_dt function formats the date time into a human readable representation in the official client
  await interaction.response.send_message(
    f'{member} joined {discord.utils.format_dt(member.joined_at)}')


# A Context Menu command is an app command that can be run on a member or on a message by
# accessing a menu within the client, usually via right clicking.
# It always takes an interaction as its first parameter and a Member or Message as its second parameter.
# This context menu command only works on messages
@client.tree.context_menu(name='Report')
async def report_message(interaction: discord.Interaction,
                         message: discord.Message):
  # We're sending this response message with ephemeral=True, so only the command executor can see it
  await interaction.response.send_message(
    f'You rat. ~~Thanks for reporting this message by {message.author.mention}.~~',
    ephemeral=True)

  # Handle report by sending it into a log channel
  log_channel = interaction.guild.get_channel(
    LOG_ID)  # replace with your channel id

  embed = discord.Embed(title='Reported Message - ' + interaction.user.name)
  if message.content:
    embed.description = message.content

  embed.set_author(name=message.author.display_name,
                   icon_url=message.author.display_avatar.url)
  embed.timestamp = message.created_at

  url_view = discord.ui.View()
  url_view.add_item(
    discord.ui.Button(label='Go to Message',
                      style=discord.ButtonStyle.url,
                      url=message.jump_url))

  await log_channel.send(embed=embed, view=url_view)
  print("New report by " + interaction.user.name)
  print("Suspect: " + message.author.name + " / " + str(message.author.id))
  print("Content: " + message.content)
  print("Message time: " + str(message.created_at))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  random_func = random.choice([
    "MY NAME IS ALEX MASON, AND I WILL HAVE MY REVENGE", "No.", "Yes.",
    "What do you mean?", "Do I look like I care",
    "Okay, but did you know that I FUCKING LOVE ALEX MASON!?",
    "No, anyways did you know that I FUCKING LOVE ALEX MASON!?",
    "Maybe give Certified Bruh Engineer some love?",
    "I'm best friends with every bot known", "ok and",
    "*numbers... the numbers...*", "I see", "w h a t", "Maybe", "Maybe not",
    "Absolutelyn't", "Absolutely!", "The fuck?!", "shit.", "I don't care",
    "I really don't care", "I really, REALLY don't care.", "shut up idc.",
    "Stop", "Begin", "i guess?", "sheeeesh", "bruh", "cool", "not really cool",
    "wtf is that delete that shit bro", "What's up", "How are you",
    "what's up how are you", "you good?",
    "https://media.discordapp.net/attachments/1018830195156860968/1052709499984679042/scott.gif",
    ""
  ])
  if client.user.mentioned_in(message) or ("kitsune".lower()) in message.content:
    await message.channel.send(str(random_func))
  return


client.run(token)
