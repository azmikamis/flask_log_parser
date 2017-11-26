from . import app
from flask import render_template, jsonify

import re

shared_data = {}
shared_data['exceptions'] = []

@app.before_first_request
def load_log_file():
    global shared_data
    filename = 'CTF1.log'
    with open(filename) as f:
        for line in f:
            try:
                date, time, local_ip, request_method, resource, remainder = line.split(' ',5)
                extras, port, remainder = re.split('\s(80|443)\s', remainder)
                _, remote_ip, remainder = remainder.split(' ', 2)
                _, user_agent, remainder = re.split('^(.+?)(?=http)', remainder)
                _, url, response, remainder = re.split('^(.+?)(?=\D(1\d{2}|2\d{2}|3\d{2}|4\d{2}|5\d{2})\D)', remainder)
                if remote_ip in shared_data:
                    shared_data[remote_ip].append(line)
                else:
                    shared_data[remote_ip] = [line]
            except:
                shared_data['exceptions'].append(line)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logs/<remote_ip>')
def getlogs(remote_ip):
    global shared_data
    response = [{'line':line} for line in shared_data[remote_ip]]
    return jsonify(response)

@app.route('/ipaddresses')
def ipaddresses():
    global shared_data
    return render_template('ipaddresses.html', ipaddresses=shared_data.keys())
