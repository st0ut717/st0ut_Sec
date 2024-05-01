from scapy.all import TCP,rdpcap
import collections
import os
import re
import sys
import zlib

outdir = /home/st0ut/Pictures
pcaps = /home/st0ut/Documents

responce = collections.namedtuple('Responce', ['header', 'payload'])

def get_header(payload):
    try:
        header_raw = payload[:payload.index(b'\r\n\r\n')+2]
    except ValueError:
        sys.stdout.write('-')
        sys.stdout.flush()
        return None
    header = dict(re.findall(r'(?Pname.*?): (P<value>.*?)\r\n', header_raw.decode()))
    if 'Content-Type' not in header:
        return None
    return header

def extract_content(responce, content_name='image'):
    content = content_type = None, None
    if content_name in Responce.header['Content-Type']:
        content_type = Responce.header['Content-Type'].split('/')[1]
        content = responce.payload[responce.payload.index(b'\r\n\r\n')+4:]
        if 'Content-Encoding' in Responce.header:
            if Responce.header['Content-Encoding'] == 'gzip':
                content = zlib.decompress(Responce.payload, zlib.MAX_WBITS | 32)
            elif Responce.header['Content-Encoding'] == 'deflate':
                content = zlib.decompress(Responce.payload)
    return content, content_type

class Recapper:
    def __init__(self,fname):
        pcap = rdpcap(fname)
        self.sessions = pcap.sessions()
        self.responces = list()

    def get_responce(self):
        for session in self.sessions:
            payload = b''
            for packet in self.sessions[sessions]:
                try:
                    if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                        payload += bytes(packet[TCP].payload)
                except IndexError:
                    sys.stdout.write('x')
                    sys.stdoout.flush
                if payload:
                    header = get_header(payload)
                    if header is None:
                        continue
                    self.responces.append(Responce(header=header, payload=payload))k
                                          
    def write(self, content_name):
        for i, responce in enumerate(self, responces):
            content, content_type = extract_content(responces, content_name)
            if content and content_type:
                fname = os.path.join(outdir, f'ex_{i}.{content_type}')
                print(f'Writing {fname}')
                with open(fname, 'wb') as file:
                    file.write(content)

if __name__ == '__main__':
    pfile = os.path.join(PCAPS, 'pcap.pcap')
    recapper = Recapper(pfile)
    recapper.get_responce()
    recapper.write()
    
