"""
    Copyright (C) 2020  Florian Thiévent
"""

import sys
from .dcc_packet_factory import DCCPacketFactory


# 11111111111111110_0_00010110_0_11000000_0_11010111

class DCCDecoder(object):
    """
    A DCC decoder takes a packet raw message and breacks it into the different data for a
    Command described in the DCC protocol electrical standard.
    """
    MICROSECOND_DIV = 1000000.0

    def __init__(self,
                 bit_one_part_min_duration=55,  # microseconds
                 bit_one_part_max_duration=61,
                 bit_one_part_duration=58,
                 bit_zero_part_min_duration=95,
                 bit_zero_part_max_duration=9900,
                 bit_zero_part_duration=100,
                 packet_separation=0):
        self.bit_one_part_min_duration = bit_one_part_min_duration
        self.bit_one_part_max_duration = bit_one_part_max_duration
        self.bit_one_part_duration = bit_one_part_duration
        self.bit_zero_part_min_duration = bit_zero_part_min_duration
        self.bit_zero_part_max_duration = bit_zero_part_max_duration
        self.bit_zero_part_duration = bit_zero_part_duration
        self.packet_separation = packet_separation

        self._payload = []
        self.idle_packet = DCCPacketFactory.idle_packet()
        self.reset_packet = DCCPacketFactory.reset_packet()
        self.stop_packet = DCCPacketFactory.stop_packet()

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, p):
        self._payload = p

    def send_idle(self, times):
        self.send_packet(self.idle_packet, times)

    def send_stop(self, times):
        self.send_packet(self.stop_packet, times)

    def send_reset(self, times):
        self.send_packet(self.reset_packet, times)

    def send_packet(self, packet, times):
        # to be implemented by subclass
        sys.stderr.write("send_packet() not implemented!")
        return False

    def send_payload(self, times):
        # to be implemented by subclass
        sys.stderr.write("send_payload() not implemented!")
        return False

    def tracks_power_on(self):
        print("Tracks powered ON")

    def tracks_power_off(self):
        print("Tracks powered OFF")
