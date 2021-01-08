"""
    Copyright (C) 2020  Florian Thiévent
"""

import bitstring


class DCCDecoder(object):
    """
    A DCC decoder takes a packet raw message and breacks it into the different data for a
    Command described in the DCC protocol electrical standard.
    """
    address = 0
    command = ""

    def __init__(self, raw_payload=None):
        if raw_payload is None:
            raw_payload = bitstring.BitArray('0b0')
        self.raw_payload = bitstring.BitArray(raw_payload)
        self.payload = bitstring.BitArray(self.cut_praeambel())
        self.set_address()
        self.set_command()

    def __str__(self):
        return "DCCPacket: Adresse %s, Kommando %s" % (self.address, self.command)

    def get_address(self):
        return self.address

    def get_command(self):
        return self.command

    def set_address(self):
        self.address = self.payload[:8].uint

    def set_command(self):
        self.command = self.payload[9:17]

    def cut_praeambel(self):
        start = 0
        for bit in self.raw_payload:
            if bit:
                start += 1
            else:
                start += 1
                break
        return self.raw_payload[start:]
