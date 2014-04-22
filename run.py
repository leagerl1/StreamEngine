import os
from flask import Flask, render_template, request, redirect
from twilio.rest import TwilioRestClient
import twilio.twiml

app = Flask(__name__)

@app.route('/_responder', methods=['GET','POST'])
def responder():
    account_sid = "AC5ef8732a3c49700934481addd5ce1659"
    auth_token = "8d29d5cc81e4062e1521237983c39b21"
    client = TwilioRestClient(account_sid,auth_token)
    sms = client.sms.messages.get("SM800f449d0399ed014aae2bcc0cc2f2ec")
    print sms.body   

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
