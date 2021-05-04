from flask import Flask, render_template, request, redirect, session, jsonify
from flask_httpauth import HTTPBasicAuth
import hashlib,binascii
from createtable import *
from loaddata import *
from algorithm import *
from decouple import config

app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    stored_password = config('hashed')
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

@app.route('/createtables')
def createtab():
    aws_access_key_id = request.headers['aws_access_key_id']
    aws_secret_access_key = request.headers['aws_secret_access_key']
    aws_session_token = request.headers['aws_session_token']

    createTables(aws_access_key_id,aws_secret_access_key,aws_session_token)
    return "True"


@app.route('/loaddata')
def loaddat():
    aws_access_key_id = request.headers['aws_access_key_id']
    aws_secret_access_key = request.headers['aws_secret_access_key']
    aws_session_token = request.headers['aws_session_token']

    loaddata(aws_access_key_id,aws_secret_access_key,aws_session_token)
    return "True"

@app.route('/algo', methods=['POST'])
@auth.login_required
def algo():
    aws_access_key_id = request.headers['aws_access_key_id']
    aws_secret_access_key = request.headers['aws_secret_access_key']
    aws_session_token = request.headers['aws_session_token']    
    app.secret_key = os.urandom(24)
    
    returnval = processAlgorithm(aws_access_key_id,aws_secret_access_key,aws_session_token)
    return returnval

if __name__ == "__main__":
    app.run()