import socket
target = input(f'Give me a target: ')
port = input(f'What port should to use? ')
int_port = int(port)
#
print(f'We have are target initiaziing client')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f'Client initialized')
print(f'Connecting to target {target} on port {port}')
client.connect((target,int_port))
print(f'send something')
client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")
print(f'get somthing')
response = client.recv(4096)
print(response.decode())
client.close
