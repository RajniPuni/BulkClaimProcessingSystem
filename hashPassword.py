import hashlib
import os
import base64
import codecs

users = {} # A simple demo storage

# Add a user
username = 'Brent' # The users username
password = 'mypassword' # The users password

salt = os.urandom(32) # A new salt for this user

key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
users[username] = { # Store the salt and key
    'salt': salt,
    'key': key
}
print(salt)

# Verification attempt 1 (incorrect password)
username = 'Brent'
password = 'mypassword'

salt = users[username]['salt'] # Get the salt
key = users[username]['key'] # Get the correct key

new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

print(new_key) # The keys are not the same thus the passwords were not the same
