import socket

# =========================== SOCKET ====================================
##==inisialisasi socket==#

def init_socket():
    port = 5005                   # Reserve a port for your service.
    ss = socket.socket()             # Create a socket object
    host = socket.gethostname()     # Get local machine name
    # host = '192.168.43.26'     # Get local machine name
    ss.bind((host, port))            # Bind to the port
    ss.listen(100)                    # Now wait for client connection.
    return ss


def sendtext(text, ss):
    print('Server listening....')
    conn, addr = ss.accept()     # Establish connection with client.
    print('Got connection from', addr)
    data = conn.recv(1024)
    print('Server received', repr(data))
    print('Sending file to client')
# filename='index.csv'
    conn.send(text)
    # print(text.decode())
    conn.close()

def socketsend(filename, ss):
    print('Server listening....')
    conn, addr = ss.accept()     # Establish connection with client.
    print('Got connection from', addr)
    data = conn.recv(30)
    print('Server received', repr(data))
    print('Sending file to client')
# filename='index.csv'
    conn.send(str.encode(filename))
    f = open(filename, 'rb')
    l = f.read(2048)
    while (l):
        conn.send(l)
        l = f.read(2048)
    print('File SUCCESFULLY sent')
    print('Done sending')
    conn.close()

## TERIMA DATA ##


def socketrecv(ss):
    ss.listen(5)
    print('Server listening....')
    conn, addr = ss.accept()     # Establish connection with client.
    path = conn.recv(1024)
    print('Got connection from', addr)
    print('Receiving from client', path)
    with open(path, 'wb') as g:
        print('file opened')
        print('receiving data...')
        while True:
            data = conn.recv(1048)
            if not data:
                break
            # write data to a file
            g.write(data)
    g.close()
    print('Successfully get the file')
    conn.close()