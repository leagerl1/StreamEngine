import os
from flask import Flask, render_template, request, redirect
from twilio.rest import TwilioRestClient
import twilio.twiml

app = Flask(__name__)

@app.route('/_responder', methods=['GET','POST'])
def responder():
    account_sid = "ACfe656ed49f19a12b8440cb191158f0c9"
    auth_token = "8d29d5cc81e4062e1521237983c39b21"
    client = TwilioRestClient(account_sid, auth_token)
    sms = client.messages.get("SMbb7efe0e6b3c545245ee6d6cb5944364")
    return message.body

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
