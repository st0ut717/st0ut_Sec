import socket
import os

#Host to listen on
HOST = '100.115.92.203'

def main():
    # Crate raw socket, bin to public interface
    if os.name = 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((HOST, 0))
    # include IP header in capture
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    if os.name = 'nt':
        sniffer.ioctl(socket.SID_RCVALL, socket.RCVALL_ON)
    