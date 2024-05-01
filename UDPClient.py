import socket
target = "127.0.0.1"
port = 9997
#
print(f'We have the target initiaziing client')
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(f'Client initialized')
print(f'send something')
client.sendto(b"AAABBBCCC",(target,port))
print(f'get somthing')
data, addr = client.recvfrom(4096)
print(data.decode())
client.close