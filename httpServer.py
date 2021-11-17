"""
HTTP Server socket program
"""
import socket
import os
import sys
import datetime
import threading

# getting the current date and time
today = datetime.datetime.now()

# response headers
conn = 'Connection: keep-alive\n'
date = str(today)+' EST\n'
server = 'Server: Apache\n'
response_content = 'Content-Type: text/html; charset=iso-8859-1\n\n'

# getting the address which this server is running on
server_address = socket.gethostbyname(socket.gethostname())

# making sure the port arg was initialized with the command line
if len(sys.argv) < 2:
    print('...failed to enter port number. Exiting program')
    sys.exit()

# initializing the port number
server_port = int(sys.argv[1])

# creating the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((server_address, server_port))
server_socket.listen(1)
print('Listening on port %s ...' % server_port)

# setting the condition for the connection loop to True
loop = True


# function for identifying user input to kill the server
def key_capture_thread():
    global loop
    input()
    loop = False


# loop function for looking for connections to the server
def loop_for_connection():

    while loop:

        # starting thread for user input
        threading.Thread(target=key_capture_thread, args=(), name='key_capture_thread', daemon=True).start()

        # because a connection has not been made connection made is initially set to false
        connection_made = False

        # setting the socket timeout so that it doesn't just sit looking forever
        server_socket.settimeout(1)
        try:
            # start looking for a connection and state it is successful upon connection
            client_connection, client_address = server_socket.accept()
            connection_made = True
            print('**Connection Made** \n')
        except socket.error:
            pass

        # if a valid connection was made read the request and send data based on the given method
        if connection_made:
            request = client_connection.recv(1024).decode()

            # breaking the request into its different parts
            request_l1 = request.partition('\n')[0]
            method, _, rest = request_l1.partition(' ')
            file, _, protocol = rest.partition(' ')

            print(request_l1+'\r\n\r\n')

            # sending the response based on the given method
            if method == 'GET':
                if file == '/' or file == '/index.html':
                    # open file and get content
                    fin = open('index.html')
                    content = fin.read()
                    fin.close()

                    # send response with the file content
                    response = 'HTTP/1.0 200 OK\n'+conn+date+server+response_content+content
                    client_connection.sendall(response.encode('utf8'))

                elif os.path.isfile('.'+file):
                    # open file and get content
                    fin = open('.'+file)
                    content = fin.read()
                    fin.close()

                    # send response with the file content
                    response = 'HTTP/1.0 200 OK\n'+conn+date+server+response_content+content
                    client_connection.sendall(response.encode('utf8'))

                else:
                    # if file isn't found send 404 not found
                    response = 'HTTP/1.0 404 Not Found\n'+conn+date+server+response_content+'<h1>404 File Not Found</h1>'
                    client_connection.sendall(response.encode())

            # if method is put
            elif method == 'PUT':
                file_name = file.replace('/', '')

                index = request.find('<')
                last_index = len(request)-1
                data = request[index:last_index]

                # create new file get given file data and save to current directory
                if os.path.isfile('.'+file):
                    file_save = open('.'+file)
                    content = file_save.read()
                    if content == data:
                        response = 'HTTP/1.0 204 No Content\n' + 'Content-Location: ' + file + '\r\n\r\n'
                        client_connection.sendall(response.encode())
                        file_save.close()
                    else:
                        file_save.close()
                        file_save = open('.'+file, 'w')
                        file_save.write(data)
                        file_save.close()
                        response = 'HTTP/1.0 200 OK\n' + 'Content-Location: ' + file + '\r\n\r\n'
                        client_connection.sendall(response.encode())

                else:
                    file_save = open(file_name, "w")
                    file_save.write(data)
                    file_save.close()

                    # send response saying the file was created
                    response = 'HTTP/1.0 201 Created\n'+'Content-Location: '+file+'\r\n\r\n'
                    client_connection.sendall(response.encode())

            # close the client connection
            client_connection.close()


# start the search for a client connection and prompt for how to stop it
print("To kill the server press Enter...")
loop_for_connection()

# if server is terminated close the socket and end the program
server_socket.close()
print("Server terminated...")

