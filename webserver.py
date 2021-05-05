from flask import Flask
from flask import request, make_response, jsonify
from threading import Thread
from database import spendDiscordDollarsChrome

app = Flask('Discord Bot Webserver')

#homepage
@app.route('/')
def home():
    return "Hello. I am alive!"

#respond to Chrome extension request, dock a DiscordDollar for specified user
@app.route('/users/<user_id>', methods = ['GET', 'POST', 'OPTIONS'])
def user(user_id):
  if request.method == 'OPTIONS':
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

  if request.method == 'GET':
    print("GET from " + user_id + "!")
    return "Get request received!"

  elif request.method == 'POST':
    data = request.json
    response = make_response(jsonify("POST received!"))
    print("POST received! " + data['id'])
    response.headers.add("Access-Control-Allow-Origin", "*")
    spendDiscordDollarsChrome(data['id'], 1)
    return response

  else:
    return "Method not allowed!"

def run():
  app.run(host='0.0.0.0',port=8080)

#run the webserver
def webserver():
    t = Thread(target=run)
    t.start()
