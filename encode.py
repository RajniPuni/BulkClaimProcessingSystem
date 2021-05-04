import base64

message = "\xa4v\x94\xf7'a\xb7\xca\xcc\x86\xfdq\xab\x0e!\x04v\x8a\x9e\xd5#\xbd\xff;\xfe\xb2g\x87W\xd5\xa7$"
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode('ascii')

print(base64_message)


base64_bytes = base64_message.encode('ascii')
message_bytes = base64.b64decode(base64_bytes)
message = message_bytes.decode('ascii')

print(message)