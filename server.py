#!/usr/bin/env python 
import socket
import threading
from struct import *

class DNSQuery(object):

    def __init__(self):
        pass

    @classmethod
    def from_data(cls, data):
        self = cls()
        self.id = int(data[0:2].encode('hex'), 16)
        self.flag = int(data[2:4].encode('hex'), 16)

        self.qr =     self.flag & 0b1000000000000000
        self.opcode = self.flag & 0b0111100000000000
        self.aa =     self.flag & 0b0000010000000000
        self.tc =     self.flag & 0b0000001000000000
        self.rd =     self.flag & 0b0000000100000000
        self.ra=      self.flag & 0b0000000010000000
        self.z =      self.flag & 0b0000000001000000
        self.ad =     self.flag & 0b0000000000100000
        self.cd =     self.flag & 0b0000000000010000
        self.rcode =  self.flag & 0b0000000000001111

        self.question = int(data[4:6].encode('hex'), 16)
        self.answer_rrs = int(data[6:8].encode('hex'), 16)
        self.authority_rrs = int(data[8:10].encode('hex'), 16)
        self.addtional_rrs = int(data[10:12].encode('hex'), 16)

        i = 12
        self.name = ""
        while data[i:i+1].encode('hex') != "00":
            self.name += data[i:i+1]
            i += 1


        i += 1
        self.type = int(data[i:i+2].encode('hex'), 16)
        self._class = int(data[i+2:i+4].encode('hex'), 16)

        return self

    def __getitem__(self, item):
        return getattr(self, item)

    def __repr__(self):
        return "Transaction ID:{}".format(hex(self.id))

    def __str__(self):
        flag = 0
        flag += self.qr &       0b1000000000000000
        flag += self.opcode &   0b0111100000000000
        flag += self.aa &       0b0000010000000000
        flag += self.tc &       0b0000001000000000
        flag += self.rd &       0b0000000100000000
        flag += self.ra &       0b0000000010000000
        flag += self.z &        0b0000000001000000
        flag += self.ad &       0b0000000000100000
        flag += self.cd &       0b0000000000010000
        flag += self.rcode &    0b0000000000001111



if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 53))

    while 1:
        data, addr = sock.recvfrom(1000)
        query = DNSQuery.from_data(data)
