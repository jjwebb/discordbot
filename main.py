import discord
from discord.ext import tasks, commands
import os
import re
from scraping import etymology, btcPrice, btcPriceForeign, dictionary, urbanDictionary, translate, getGarfield, getDilbert, getGoComic
from database import getMembers, addDiscordDollars, spendDiscordDollars, buyBitcoin, sellBitcoin, sendCurrency, getChromeCode
from webserver import webserver
from minesweeper import minesweeper

client = commands.Bot(command_prefix='$')

#print bot info on login success
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  print('{0.user}'.format(client))

#globals for connect four game tracking
connect4Msg = ""
connect4arr = ""
connect4txt = ""
connect4 = False
redTurn = False
connect4player1 = ""
connect4TwoPlayers = False

#check if a player has won connect 4
def connect4win(row, col):
  global connect4arr
  if (checkDirection(row, col,  1,  1) == 3 or
      checkDirection(row, col,  0,  1) == 3 or
      checkDirection(row, col, -1,  1) == 3 or
      checkDirection(row, col, -1,  0) == 3 or
      checkDirection(row, col, -1, -1) == 3 or
      checkDirection(row, col,  0, -1) == 3 or
      checkDirection(row, col,  1, -1) == 3 or
      checkDirection(row, col,  1,  0) == 3):
    return True
  else:
    return False

#recursive connect 4 grid checker
def checkDirection(row, col, rowdir, coldir):
  global connect4arr
  if (-1 < row + rowdir < 7) and (-1 < col + coldir < 7):
    if connect4arr[row][col] == connect4arr[row+rowdir][col+coldir]: 
      return 1 + checkDirection(row+rowdir, col+coldir, rowdir, coldir)
    else:
      return 0
  else:
    return 0

#connect 4 game
async def connectfour(message, colNum):
  global connect4txt
  global connect4arr
  global connect4Msg
  global connect4
  global redTurn
  msg = ""
  won = False

  #enter the move and check for a win
  if 0 < colNum < 8:
    for row in range(6):
      if connect4arr[5-row][colNum-1] == 0:
        connect4arr[5-row][colNum-1] = 8 if redTurn else 9
        if connect4win(5-row, colNum-1):
          won = True
          print("You won!")
          break
        redTurn = not redTurn
        break

  #convert grid to string
  for row in range(7):
    for col in range(7):
      if connect4arr[row][col] == 0:
        msg += "⚪ "
      elif connect4arr[row][col] == 1:
        msg += "1️⃣ "
      elif connect4arr[row][col] == 2:
        msg += "2️⃣ "
      elif connect4arr[row][col] == 3:
        msg += "3️⃣ "
      elif connect4arr[row][col] == 4:
        msg += "4️⃣ "
      elif connect4arr[row][col] == 5:
        msg += "5️⃣ "
      elif connect4arr[row][col] == 6:
        msg += "6️⃣ "
      elif connect4arr[row][col] == 7:
        msg += "7️⃣ "
      elif connect4arr[row][col] == 8:
        msg += "🔴 "
      elif connect4arr[row][col] == 9:
        msg += "🔵 "
      else:
        msg += str(connect4arr[row][col])
    msg += "\n"

  if not won:
    msg += "RED's turn" if redTurn else "BLUE's turn"
  else:
    msg += "RED wins!\n" if redTurn else "BLUE wins!\n"
    if connect4TwoPlayers:
       msg += message.author.display_name + " gets 200 DiscordDollars!"
       addDiscordDollars(message.author.id, 200)
    else:
      msg += "Nice try, no DiscordDollars for you!"

    connect4 = False

  #delete the last board and move command so it doesn't clutter the chat
  connect4txt = msg
  try:
    await connect4Msg.delete()
    await message.delete()
  except:
    pass
  await message.channel.send(msg)


#process message events
@client.event
async def on_message(message):
  global connect4Msg
  global connect4

  if message.author == client.user:
    if connect4 and len(message.content) > 117:
      connect4Msg = message
    return
  
  #automatically respond to "yeah but"s
  elif "yeah but" in message.content.lower().replace(",", ""):
    await message.channel.send("Yeahbuts live in the woods.")
    spendDiscordDollars(message.author.id, 50)

  #start a connect four game
  elif message.content.startswith('CONNECT FOUR'):
    global connect4arr
    global connect4TwoPlayers
    global connect4player1
    if connect4 == False:
      connect4arr =  [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [1, 2, 3, 4, 5, 6, 7]]
      connect4 = True
      connect4TwoPlayers = False
      connect4player1 = message.author.id
    await connectfour(message, 0)

  #play connect 4 move (1-7) if a game is already underway
  elif message.content.isnumeric() and 0 < int(message.content) < 8:
    if connect4:
      if message.author.id != connect4player1: connect4TwoPlayers = True
      await connectfour(message, int(message.content))
      return

  #generate minesweeper board
  elif message.content.startswith('MINESWEEPER'):
    await message.channel.send(minesweeper())
  
  #pull garflied comic from Garflied archive
  elif message.content.startswith('GARFIELD PLEASE'):
    await message.channel.send(getGarfield())
    spendDiscordDollars(message.author.id, 5)

  #random Dilbert strip
  elif message.content.startswith('DILBERT PLEASE'):
    await message.channel.send(getDilbert())
    spendDiscordDollars(message.author.id, 5)

  #random C&H
  elif message.content.startswith('CALVIN AND HOBBES PLEASE'):
    await message.channel.send(getGoComic("calvinandhobbes"))

  #respond to @s
  elif client.user.mentioned_in(message):
    await message.channel.send('Hi!')
  
  #add one to DiscordDollar count just for sending a message, process other commands
  addDiscordDollars(message.author.id, 1)
  await client.process_commands(message)



#command list
@client.command()
async def harvhelp(ctx):
  await ctx.send("""MINESWEEPER: generate minesweeper board\n
                    CONNECT FOUR: play connect 4\n
                    GARFIELD PLEASE: random Garfield strip\n
                    DILBERT PLEASE: random Dilbert strip\n
                    CALVIN AND HOBBES PLEASE: random C&H\n
                    $comic [comic]: random comic from GoComics\n
                    $ety [word]: etymology lookup\n
                    $def [word]: dictionary lookup\n
                    $udef [word]: Urban Dictionary lookup\n
                    $bitcoin: get current btc price\n
                    $bitcoinx [xxx]: get btc price in foreign currency\n
                    $buybitcoin [amount]: buy Bitcoin with DiscordDollars\n
                    $sellbitcoin [amount]: sell Bitcoin for DiscordDollars\n
                    $send [@user] [amount] [dd, btc]: send BTC or DD to another user\n
                    $trans \"your message here\" [language]: translate message\n
                    $dd: check your DiscordDollars balance\n
                    $chromecode: get a code to link the Chrome extension to Discord\n
                    $help: show commands""")

#word etymology lookup
@client.command()
async def ety(ctx, word):
  await ctx.send(etymology(word))

#Merriam Webster lookup
@client.command(name="def")
async def define(ctx, word):
  await ctx.send(dictionary(word))

#Urban Dictionary lookup
@client.command()
async def udef(ctx, word):
  await ctx.send(urbanDictionary(word))

#get the current price of Bitcoin
@client.command()
async def bitcoin(ctx):
  await ctx.send(btcPrice())

#buy Bitcoin with DiscordDollars
@client.command()
async def buybitcoin(ctx, amount=0.0):
  price = float(re.sub(r'[^\d.]', '', btcPrice())) / 100
  await ctx.send(buyBitcoin(ctx.author.id, amount, price))

#sell Bitcoin for DiscordDollars
@client.command()
async def sellbitcoin(ctx, amount=0.0):
  price = float(re.sub(r'[^\d.]', '', btcPrice())) / 100
  await ctx.send(sellBitcoin(ctx.author.id, amount, price))

#send currency from one member to another
@client.command()
async def send(ctx, user: discord.User, amount, currency="dd"):
  uid = user.id
  await ctx.send(sendCurrency(ctx.author.id, uid, amount, currency))

#get Bitcoin price in foreign currency (default CAD)
@client.command()
async def bitcoinx(ctx, currency="cad"):
  if currency.lower() in ("discorddollars", "dd"):
    value = float(re.sub(r'[^\d.]', '', btcPrice()))
    await ctx.send("₩{:,.2f}".format(value / 100))
  else:
    await ctx.send(btcPriceForeign(currency))

#get Bitcoin price in CAD
@client.command()
async def bitcoincad(ctx, currency="cad"):
  await ctx.send(btcPriceForeign(currency))

#get a comic from GoComics
@client.command()
async def comic(ctx, comic):
  if spendDiscordDollars(ctx.author.id, 10):
    await ctx.send(getGoComic(comic))
  else:
    await ctx.send("You don't have enough DiscordDollars to do that!")

#translate a string using google translate
@client.command()
async def trans(ctx, str, lang="en"):
  await ctx.send(translate(str, lang))

#get DiscordDollars and Bitcoin (if any) owned by users
@client.command()
async def dd(ctx):
  members = getMembers()
  msg=""
  for m in members:
    user = await client.fetch_user(m[0])
    msg+=str(user.display_name) + ": $" + str(m[1]) 
    if m[2] > 0.0: msg += " ₿" + str(m[2]) 
    msg += "\n"
  await ctx.send(msg)

#issue a unique ChromeCode for use with the Chrome extension
@client.command()
async def chromecode(ctx):
  await ctx.send(getChromeCode(ctx.author.id))

#run the bot
webserver()
client.run(os.getenv('TOKEN'))