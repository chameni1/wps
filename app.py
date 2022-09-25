import requests
import re
from rq import Queue
from rq.job import Job
from flask import Flask, render_template, request, jsonify,url_for
from flask_restful import Api, Resource
import json
import html
app = Flask(__name__)
@app.route('/', methods=['GET'])
def form():
    return render_template('form.html')
# read file
with open('Result/pentest.id/cms.json', 'r') as myfile:
    data = myfile.read()
@app.route("/index",methods=['GET'])
def index():
    return render_template('index.html', title="page", jsonfile=json.dumps(data,indent=2))  
if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)
