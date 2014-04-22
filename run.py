import os
from flask import Flask, render_template, request, redirect
from twilio.rest import TwilioRestClient
import twilio.twiml

app = Flask(__name__)

@app.route('/_responder', methods=['GET','POST'])
def responder():
    resp = twilio.twiml.Response()
    message = request.values.get('Body')
    resp.message("Hello")
    return str(message)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
