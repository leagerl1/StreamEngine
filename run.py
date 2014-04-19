import os
from flask import Flask, render_template, request, redirect
import twilio.twiml

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    resp = twilio.twiml.Response()
    resp.message("Hello, Mobile Monkey")
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
