from bitstring import Bits, BitArray


class MFXDecoder(object):
    packet = ""
    address = 0
    address_bits_num = 0
    address_bits = []
    command = ""
    command_bits = []
    direction = None
    direction_bit = ""
    dataframe = []
    parameters = ""
    fnr = None
    fnr_bit = ""

    def __init__(self, packet):
        self.packet = packet
        self.set_address()
        self.set_command()
        self.check_checksum()

    def __str__(self):
        if self.direction is not None:
            return "MFXPacket: Lokadresse %s, Kommando %s, Richtung %s, Parameter %s" % (self.address, self.command, self.direction, self.parameters)
        elif self.fnr is not None:
            return "MFXPacket: Lokadresse %s, Kommando %s, Funktionen %s" % (self.address, self.command, self.fnr)
        else:
            return "MFXPacket Lokadresse %s Kommando %s" % (self.address, self.command)

    def get_address(self):
        return self.address

    def get_command(self):
        return self.command

    def get_direction(self):
        return self.direction

    def remove_praeambel(self):
        packet = self.packet
        eb = 0
        pos = 0
        for b in packet:
            pos += 1
            if b:
                if eb == 3:
                    return packet[(pos + 1):]
                eb += 1

    def set_address(self):
        packet = self.remove_praeambel()
        if str(packet[:4]) == '1000':
            self.address = int(packet[2:9], 2)
            self.address_bits = packet[2:9]
            self.address_bits_num = 9
        if str(packet[:4]) == '1100':
            self.address = int(packet[3:12], 2)
            self.address_bits = packet[3:12]
            self.address_bits_num = 12
        if str(packet[:4]) == '1110':
            self.address = int(packet[4:15], 2)
            self.address_bits = packet[4:15]
            self.address_bits_num = 15
        if str(packet[:4]) == '1111':
            self.address = int(packet[4:18], 2)
            self.address_bits = packet[4:18]
            self.address_bits_num = 19

    def set_command(self):
        packet = self.remove_praeambel()
        self.get_address()

        self.command_bits = packet[(self.address_bits_num):(self.address_bits_num + 3)]
        self.dataframe = packet[(self.address_bits_num + 3):]
        if str(self.command_bits) == '000':
            self.command = 'Fahren (kurz)'
            self.set_direction()
            self.set_parameters_fahren_kurz()
        elif str(self.command_bits) == '001':
            self.command = 'Fahren'
            self.set_direction()
            self.set_parameters_fahren()
        elif str(self.command_bits) == '010':
            self.command = 'Funktionen (kurz)'
            self.set_parameters_funktionen_kurz()
        elif str(self.command_bits) == '011':
            self.command = 'Funktionen (erweitert)'
            self.set_parameters_funktionen_erweitert()
        elif str(self.command_bits) == '100':
            self.command = 'Funktionen (Einzelansteuerung)'
            self.set_parameters_funktionen_einzel()
        elif str(self.command_bits) == '101':
            self.command = 'reserviert'
            self.set_parameters_not_used()
        elif str(self.command_bits) == '110':
            self.command = 'reserviert'
            self.set_parameters_not_used()
        elif str(self.command_bits) == '111':
            self.command = 'Konfiguration'
            self.set_parameters_konfiguration()
        else:
            raise Exception("Do not know this command")

    def set_parameters_fahren_kurz(self):
        params = self.dataframe[1:5]
        while len(params) is not 8:
            params = params + '0'
        self.parameters = 'Fahrstufe %d' % (int(params, 2) / 16)

    def set_parameters_fahren(self):
        params = self.dataframe[2:10]
        self.parameters = 'Fahrstufe %d' % (int(params, 2))

    def set_parameters_funktionen_kurz(self):

        funcs = self.dataframe[:4]
        f0, f1, f2, f3, = ("off", "off", "off", "off")

        if funcs[0] == '1':
            f3 = "on"
        if funcs[1] == '1':
            f2 = "on"
        if funcs[2] == '1':
            f1 = "on"
        if funcs[3] == '1':
            f0 = "on"

        self.fnr = {"f0": f0, "f1": f1, "f2": f2, "f3": f3}

    def set_parameters_funktionen_erweitert(self):
        pass

    def set_parameters_funktionen_einzel(self):
        funnr = self.dataframe[:8]
        funstate = self.dataframe[8:9]

        state = "off"
        if funstate == '1':
            state = "on"
        fnr = "F%d" % int(funnr, 2)
        self.fnr = {fnr: state}

    def loco_func_state(self, func):
        if func == 1:
            return True
        return False

    def set_parameters_konfiguration(self):
        self.parameters = "Konfiguration wird nicht unterstützt"

    def set_parameters_not_used(self):
        self.parameters = "Funktion wird aktuell nicht genutzt oder reserviert"

    def get_parameters(self):
        return self.parameters

    def set_direction(self):
        direc = str(self.dataframe[0])
        self.direction_bit = self.dataframe[0]
        if direc == '0':
            self.direction = 'vorwärts'
        elif direc == '1':
            self.direction = 'rückwärts'
        else:
            self.direction = 'Richtung kann nicht bestimmt werden'

    def check_checksum(self):
        chk_ok = False
        '''
        chk_from_paket = BitArray(self.packet[-13:-5])
        addr = BitArray(self.address_bits)
        data = BitArray(self.dataframe)
        '''

        return chk_ok
