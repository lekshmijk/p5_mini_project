import socket
import sys
from datetime import datetime
import csv
import numpy
import pandas
import xml.etree.ElementTree as et

# https://realpython.com/python-sockets/
# https://pymotw.com/2/socket/tcp.html
# https://www.thepythoncode.com/article/send-receive-files-using-sockets-python
# https://docs.python.org/3/library/xml.etree.elementtree.html



host = '127.0.0.1' #ip address
port = 10000       #port number 
buffer_size = 4096
file_to_client = "processing_times_table.csv"   #file beign send to client

save_file = open("save","w")    #open a file to write data receiving from server

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:  #create tcp server socket
    sock.bind((host,port)) #bind socket to address
    print("Waiting to establish a connection...")
    sock.listen() #enable server to accept connections
    client_conn, client_addr = sock.accept() #if any, accept connections
    with client_conn:
        print(f"Connection established with {client_addr}")
        while True:
            data = client_conn.recv(buffer_size).decode()  #receive data info using the client socket
            filename = data
            print("data received from server:", filename)  
            if not data:
                break
            else:
                with open(filename, "wb") as f:    #receive actual data from the file through socket 
                    bytes_read = client_conn.recv(buffer_size) #read the bytes received from socket
                    f.write(bytes_read) #write the bytes received to the file
                ##########################################################################
                tree = et.parse(filename)       #parse the data received
                root = tree.getroot()           
                for info in root.findall('info'):    #find all the necessary elements 
                    n1 = info.find('number1').text
                    n2 = info.find('number2').text
                    name = info.get('name')
                    print(name, ':', n1 , ',', n2)   #print on screen
                    today = datetime.now()
                    save_file.write(str(today) + '\t' + name + ':' + n1 + ',' + n2 + '\n')   #write the data received in file
                ###########################################################################
                client_conn.send(f"{file_to_client}".encode())
                with open(file_to_client,"rb") as f2:
                    reader = f2.read(buffer_size)
                    client_conn.sendall(reader)
                ############################################################################
        save_file.close()
    client_conn.close()
sock.close()

 
