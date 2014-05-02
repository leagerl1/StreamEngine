import os
from flask import Flask, render_template, request, redirect
from twilio.rest import TwilioRestClient
import twilio.twiml
import requests
import json
from rdio import Rdio

app = Flask(__name__)

@app.route('/_text',methods=['GET','POST'])
def hello_monkey():
    resp = twilio.twiml.Response()
    resp.message("Hello, mobile monkey")
    return str(resp)

@app.route('/_responder', methods=['GET','POST'])
def responder():
    ec_r = requests.get("https://ACfe656ed49f19a12b8440cb191158f0c9:8d29d5cc81e4062e1521237983c39b21@api.twilio.com/2010-04-01/Accounts/ACfe656ed49f19a12b8440cb191158f0c9/SMS/Messages.json")
    data = json.loads(ec_r.text)
    song = data['sms_messages'][0]['body']
    return render_template('app.html', song = song)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
