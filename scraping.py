import requests
import re
from bs4 import BeautifulSoup
import json
import random

#automatic import of google-trans-new fails on repl.it, this fixes it
try:
    from google_trans_new import google_translator
except ModuleNotFoundError:
    import os
    os.system('pip install google-trans-new')
    from google_trans_new import google_translator

translator = google_translator()
with open("langs.json", "r") as f:
  langs = json.load(f)

#$trans "your string here" [language]: translate string into selected language
def translate(str, lang):
  if lang.lower() in langs:
    lang = langs[lang]
  try:
    return translator.translate(str, lang_tgt=lang)
  except:
    return "couldn't get translation!"

#$ety [word]: get the etymology of a word
def etymology(word):
  page = requests.get('https://www.etymonline.com/search?q=' + word)
  soup = BeautifulSoup(page.content, 'html.parser')

  defs = soup.find_all('section', class_='word__defination--2q7ZH undefined')

  try:
    return defs[0].text
  except:
    return "couldn't get etymology!"

#$def [word]: get Merriam Webster definition of a word
def dictionary(word):
  page = requests.get('https://www.merriam-webster.com/dictionary/' + word)
  soup = BeautifulSoup(page.content, 'html.parser')

  defs = soup.find_all('div', class_='vg')
  try:
    str = defs[0].text
    str = re.sub(r'\n+\s*\n*', r'\n', str)
    str = re.sub(r'([1-9]?[abcdef]?)\n:', r'\1:', str)
    return str
  except:
    return "couldn't get definition!"

#$udef [word]: get Urban Dictionary definition of a word
def urbanDictionary(word):
  page = requests.get('https://www.urbandictionary.com/define.php?term='+word)
  soup = BeautifulSoup(page.content, 'html.parser')

  for br in soup.find_all("br"):
    br.replace_with("\n")
  defs = soup.find_all('div', class_='meaning')
  examples = soup.find_all('div', class_='example')
  try:
    str = defs[0].text + '\n*' + examples[0].text + '*'
    str = re.sub(r'\n+', '\n', str)
    return str
  except:
    return "couldn't get definition!"

#$bitcoin: get price of bitcoin in USD
def btcPrice():
  page = requests.get('https://www.coindesk.com/price/bitcoin')
  soup = BeautifulSoup(page.content, 'html.parser')

  defs = soup.find_all('div', class_='price-large')

  try:
    return defs[0].text
  except:
    return "couldn't get price!"

#$bitcoinx [currency]: get price of bitcoin in foreign currency
def btcPriceForeign(currency):
  page = requests.get('https://www.coingecko.com/en/coins/bitcoin/'+currency)
  soup = BeautifulSoup(page.content, 'html.parser')

  defs = soup.find_all('span', class_='no-wrap')
  try:
    return defs[0].text
  except:
    return "couldn't get price!"

#GARFIELD PLEASE: get random Garfield strip
def getGarfield():
  year = random.randint(1978, 2021)
  month = random.randint(1, 12)
  day = random.randint(1, 31)
  if day == 31 and month in [4, 6, 9, 11]:
    day = day - 1
  elif day > 28 and month == 2:
    day = 28
  url = "http://images.ucomics.com/comics/ga/" + str(year) + "/ga"
  url += "%02d" % (year - 1900) if year < 2000 else "%02d" % (year - 2000)
  url += "%02d" % month
  url += "%02d" % day + ".gif"
  return url

#DILBERT PLEASE: get random Dilbert strip
def getDilbert():
  year = random.randint(1989, 2021)
  month = random.randint(1, 12)
  day = random.randint(1, 31)
  if day == 31 and month in [4, 6, 9, 11]:
    day = day - 1
  elif day > 28 and month == 2:
    day = 28
  url = "https://dilbert.com/strip/" + str(year) + "-"
  url += "%02d" % month + "-"
  url += "%02d" % day
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')
  defs = soup.find_all('img', class_='img-responsive img-comic')
  try:
    return defs[0]['src']
  except:
    return "couldn't get image!"

#$comic [comic]: get random specified comic hosted on GoComics
def getGoComic(comic):
  comic = re.sub(r'([^\w])','', comic.lower())
  page = requests.get("https://www.gocomics.com/random/"+comic)
  return page.url