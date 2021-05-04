from flask import Flask
from flask_httpauth import HTTPBasicAuth
import hashlib
import os

app = Flask(__name__)
auth = HTTPBasicAuth()



@auth.verify_password
def verify_password(username, password):
    salt = b'\'\x82DV+\xea/)L|\xd5\xb0"\xe5\tI\xf7\xceI\xfd-\x142\xd1\x03\tX!\x14}\xf6W'
    key = b'\xbd\x15e\xa7E\x80\x15\x13<j6`\xb8c\xf8\xd9Ru\xb6\x0e\x06\xa2\x14$\xcd\x16-\x8c\xae\xd1h\xba'
    
    new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    print(new_key)
    print(key)
    if key == new_key:
        return True
    else:
        return False

@app.route('/auth', methods=['POST'])
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())

if __name__ == '__main__':
    app.run()