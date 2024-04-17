import pyvisa
print(1)

class Agilent_n6701a(object):
    def __init__(self):
        self.instruments = pyvisa.ResourceManager()
        self.agilent_n6701a = self.instruments.open_resource('USB0::0x0957::0x0C07::MY45001066::INSTR')

    def query_settings(self, channel: int, toPrint: bool = False):
        self.agilent_n6701a.write('CURRent? (@' + str(channel) + ')')
        current = float(self.agilent_n6701a.read())
        self.agilent_n6701a.write('VOLTage? (@' + str(channel) + ')')
        voltage = float(self.agilent_n6701a.read())

        if toPrint:
            print(f'CH{channel} setting voltage: {float(voltage)} V\n'
                  f'CH{channel} setting current: {float(current)} A\n')

        return voltage, current

    def set_settings(self, channel: int, voltage: int or float, current: int or float, output: bool):
        if output:
            self.agilent_n6701a.write('OUTPut 1, (@' + str(channel) + ')')
        else:
            self.agilent_n6701a.write('OUTPut 0, (@' + str(channel) + ')')

        self.agilent_n6701a.write(f'CURRent {current}, (@{channel})')
        self.agilent_n6701a.write(f'VOLTAge {voltage}, (@{channel})')

    def measurement(self, channel, toPrint: bool = False):
        self.agilent_n6701a.write('MEASure:VOLTage? (@' + str(channel) + ')')
        voltage = float(self.agilent_n6701a.read())
        self.agilent_n6701a.write('MEASure:CURRent? (@' + str(channel) + ')')
        current = float(self.agilent_n6701a.read())

        if toPrint:
            print(f'CH{channel} meas voltage: {float(voltage)} V\n'
                  f'CH{channel} meas current: {float(current)} A\n')

        return voltage, current


if __name__ == '__main__':
    agilent_n6701 = Agilent_n6701a()
    # agilent_n6701.set_settings(channel=1, voltage=2, current=2, output=True)
    # agilent_n6701.query_settings(channel=1, toPrint=True)
    agilent_n6701.measurement(channel=1, toPrint=True)
