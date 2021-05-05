import sqlite3
import random

connection = sqlite3.connect('members.db', check_same_thread=False)

cursor = connection.cursor()

command1 = """CREATE TABLE IF NOT EXISTS
members(userID INTEGER PRIMARY KEY, discordDollars INTEGER NOT NULL DEFAULT 0, bitcoin REAL NOT NULL DEFAULT 0.0,
chromeCode INTEGER UNIQUE)"""

cursor.execute(command1)
connection.commit()

#add a member to the database
def addMember(memberID):
  with connection:
    cursor.execute("INSERT OR IGNORE INTO members VALUES (?, ?, ?)", (memberID, 0, 0.0))

#add specified number of DiscordDollars to the specified user's account
def addDiscordDollars(memberID, number=1):
  with connection:
    cursor.execute("INSERT OR IGNORE INTO members VALUES (?, ?, ?, ?)", (memberID, 0, 0.0, None))
    cursor.execute("UPDATE members SET discordDollars = discordDollars + ? WHERE userID = ?",(number, memberID))

#returns false if user does not have enough DiscordDollars
def spendDiscordDollars(memberID, number=1):
  with connection:
    cursor.execute("INSERT OR IGNORE INTO members VALUES (?, ?, ?, ?)", (memberID, 0, 0.0, None))
    cursor.execute("SELECT discordDollars FROM members WHERE userID = ?", (memberID,))
    num = cursor.fetchone()[0]
    print(num)
    if num < number: return False
    cursor.execute("UPDATE members SET discordDollars = discordDollars - ? WHERE userID = ?",(number, memberID))
    return True;

#send currency from one member to another
def sendCurrency(memberSend, memberReceive, amount, currency):
  if currency.lower() in ('btc', 'bitcoin', 'bitcoins', 'b'):
    currency = 'bitcoin'
    amount = float(amount)
    if amount < 0.01:
      return "Can't send less than 0.01 btc!"

  elif currency.lower() in ('dd', 'discorddollar', 'discorddollars', 'd'):
    currency = 'discordDollars'
    amount = int(float(amount))
    
  else: return "Invalid currency!"
  if float(amount) < 0.0: return "Can't send a negative amount!"

  with connection:
    cursor.execute("SELECT "+currency+" FROM members WHERE userID = ?", (memberSend,))
    balance = cursor.fetchone()[0]
    if balance < amount:
      return "Not enough funds for transfer!"
    cursor.execute("UPDATE members SET "+currency+" = "+currency+" - ? WHERE userID = ?",(amount, memberSend))
    cursor.execute("UPDATE members SET "+currency+" = "+currency+" + ? WHERE userID = ?",(amount, memberReceive))
    return "Sent ;)"
    
#buy Bitcoin with DiscordDollars
def buyBitcoin(memberID, amount, price):
  if amount < 0: return "Can't buy a negative amount!"
  elif amount < 0.01: return "Can't buy less than 0.01 btc!"

  with connection:
    cursor.execute("SELECT discordDollars FROM members WHERE userID = ?", (memberID,))
    bucks = cursor.fetchone()[0]
    cost = int(amount * price)
    if bucks < cost: 
      return "Not enough DiscordDollars for transaction!"
    cursor.execute("UPDATE members SET discordDollars = discordDollars - ? WHERE userID = ?",(cost, memberID))
    cursor.execute("UPDATE members SET bitcoin = bitcoin + ? WHERE userID = ?",(amount, memberID))
  return "Bought ₿" + str(amount) + " for ₩" + str(cost) + "!"

#sell Bitcoin for DiscordDollars
def sellBitcoin(memberID, amount, price):
  if amount < 0: return "Can't sell a negative amount!"
  elif amount < 0.01: return "Can't sell less than 0.01 btc!"

  with connection:
    cursor.execute("SELECT bitcoin FROM members WHERE userID = ?", (memberID,))
    btc = cursor.fetchone()[0]
    if btc == 0.0: return "You have no Bitcoin!"
    elif btc < amount: amount = btc
    bucks = int(amount * price)
    cursor.execute("UPDATE members SET discordDollars = discordDollars + ? WHERE userID = ?",(bucks, memberID))
    cursor.execute("UPDATE members SET bitcoin = bitcoin - ? WHERE userID = ?",(amount, memberID))
  return "Sold ₿" + str(amount) + " for ₩" + str(bucks) + "!"

#get info for all members
def getMembers():
  cursor.execute("SELECT * FROM members")
  return cursor.fetchall()

#get a ChromeCode to link a member to their Chrome extension
def getChromeCode(memberID):
  code = random.randint(1000000000, 9999999999)
  with connection:
    cursor.execute("UPDATE members SET chromeCode = ? WHERE userID = ?",(code, memberID))
    cursor.execute("SELECT chromeCode FROM members WHERE userID = ?", (memberID,))
    num = cursor.fetchone()[0]
    print(num)
  return code
    
#deduct DiscordDollars using the member's ChromeCode
def spendDiscordDollarsChrome(code, number=1):
  with connection:
    cursor.execute("SELECT discordDollars FROM members WHERE chromeCode = ?", (code,))
    num = cursor.fetchone()[0]
    print(num)
    if num < number: return False
    cursor.execute("UPDATE members SET discordDollars = discordDollars - ? WHERE chromeCode = ?",(number, code))
  return True;
