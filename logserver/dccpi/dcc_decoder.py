"""
    Copyright (C) 2020  Florian Thiévent
"""

import bitstring


# 11111111111111110_0_00010110_0_11000000_0_11010111

class DCCDecoder(object):
    """
    A DCC decoder takes a packet raw message and breacks it into the different data for a
    Command described in the DCC protocol electrical standard.
    """

    def __init__(self, raw_payload=None):
        if raw_payload is None:
            raw_payload = bitstring.BitArray('0b0')
        self.raw_payload = bitstring.BitArray(raw_payload)
        self.payload = bitstring.BitArray(self.cut_praeambel())

    def get_address(self):
        return self.payload[:8].uint

    def get_command(self):
        command_byte = self.payload[9:17]
        return command_byte.bin

    def cut_praeambel(self):
        start = 0
        for bit in self.raw_payload:
            if bit:
                start += 1
            else:
                start += 1
                break
        return self.raw_payload[start:]
