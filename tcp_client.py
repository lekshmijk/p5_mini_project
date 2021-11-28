import socket
import sys
# https://www.thepythoncode.com/article/send-receive-files-using-sockets-python

buffer_size = 4096
filename = "id.xml" #file being send to server
HOST = '192.168.87.160' #ip address
PORT = 10000  #port number
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock: #create socket
    print("Connecting to:", HOST, PORT)
    sock.connect((HOST,PORT)) #connect to server 
    print("Connected!")
    sock.send(f"{filename}".encode()) #send filename we wat to send to server
    with open(filename,"rb") as data: #read bytes into socket
        reader = data.read(buffer_size)
        sock.sendall(reader)
    data = sock.recv(buffer_size).decode() #receive data info from server
    file_to_client = data
    print("data received from server:", file_to_client)
    with open(file_to_client,"wb") as f2:
        read = sock.recv(buffer_size) #read the data from socket
        f2.write(read) #write the bytes to the file
sock.close()
