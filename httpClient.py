"""
HTTP Client socket program
"""

import socket
import sys
import os

# checking to make sure the required amount of command line arguments have been entered
if len(sys.argv) < 5:
    print('Missing command line argument... program canceled')
    sys.exit()

# initializing the command line args
host = sys.argv[1] # example -> 'www.google.com' or '10.0.0.20'
port = int(sys.argv[2]) # example -> 80 or 6060
method = sys.argv[3] # example GET or PUT
file = sys.argv[4] # example index.html or any file name

# initializing the socket and exiting if it fails
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print('Failed to create socket...')
    sys.exit()

# # getting ip if address was given and exiting if fails
# try:
#     remote_ip = socket.gethostbyname(host)
# except socket.gaierror:
#     print('Hostname could not be found... program canceled')
#     sys.exit()

# connecting to server
client_socket.connect((host, port))
print('Connecting to server '+host+'...\n\n')

# sending data to server based on the entered method
if method == 'PUT':
    # opening and getting put file data
    fileData = open(file)
    content = fileData.read()
    content_length = os.path.getsize(file)
    fileData.close()

    # compiling the request string
    request = method + " /" + file + " HTTP/1.0\n"+'Content-Length: '+str(content_length)+'\r\n\r\n'+content

else:
    # compiling the request string
    request = method + " /" + file + " HTTP/1.0\r\n\r\n"

# try to send the request and exit if it fails
try:
    client_socket.sendall(request.encode())
except socket.error:
    print('Send failed...')
    sys.exit()


# get the response, format it and print it out
reply = client_socket.recv(4096).decode('utf8')
print(reply)

