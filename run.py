import os
from flask import Flask, render_template, request, redirect
from twilio.rest import TwilioRestClient
import twilio.twiml
import requests
import json
from rdio import Rdio
#import oauth2 as oauth
import urllib, cgi

app = Flask(__name__)

@app.route('/_test', methods=['GET','POST'])
def tester():
    rdio = Rdio(("u35btmntr29vd3n9hnuy9m6n", "jb8DTyHpVf"))
    url = rdio.begin_authentication('oob')
    saved_token = rdio.token
    print saved_token
    rdio = Rdio(("u35btmntr29vd3n9hnuy9m6n", "jb8DTyHpVf"), saved_token)
    #print "Go to website to verify: " + url
    #verifier = input("Enter pin: ")
    #rdio.complete_authentication(saved_token)
    print saved_token 
    song = rdio.call("search",{"query": "Lose yourself","types":"Track"})
    if(song["status"] == "ok"):
        track =  song["result"]["results"][0]["key"]
        rdio.call("addToPlaylist",{"playlist":"p8696966","tracks":str(track)})
    else:
        print "failed"
    return "Song Added"

@app.route('/_responder', methods=['GET','POST'])
def responder():
    ec_r = requests.get("https://ACfe656ed49f19a12b8440cb191158f0c9:8d29d5cc81e4062e1521237983c39b21@api.twilio.com/2010-04-01/Accounts/ACfe656ed49f19a12b8440cb191158f0c9/SMS/Messages.json")
    data = json.loads(ec_r.text)
    song = data['sms_messages'][0]['body']
    return render_template('app.html',song=song)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
