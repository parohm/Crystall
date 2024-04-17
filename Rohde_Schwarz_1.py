class Rohde_Schwarz(object):
    def __init__(self):
        import pyvisa
        self.inst = pyvisa.ResourceManager()
        self.rohde_schwarz = self.inst.open_resource('USB0::0x0AAD::0x0135::026173438::INSTR')

    def output(self, channel: int, power: bool):
        self.rohde_schwarz.write(f'INST:SELECT {channel}')

        if power == False:
            self.rohde_schwarz.write(f'OUTP 0')
        elif power == True:
            self.rohde_schwarz.write(f'OUTP 1')

    def channel_config(self, channel: int, output: bool, voltage: float, current: float):
        self.rohde_schwarz.write(f'INST:SELECT {channel}')

        if output == False:
            self.rohde_schwarz.write(f'OUTP 0')
        elif output == True:
            self.rohde_schwarz.write(f'OUTP 1')

        self.rohde_schwarz.write(f'VOLT {voltage}')
        self.rohde_schwarz.write(f'CURR {current}')

    def voltage_current_power_measurement(self, channel, toPrint: bool = False):
        self.rohde_schwarz.write(f'INST:SELECT {channel}')

        voltage = float(self.rohde_schwarz.query('MEAS:SCAL:VOLT ?'))
        current = float(self.rohde_schwarz.query('MEAS:SCAL:CURR ?'))
        power = float(self.rohde_schwarz.query('MEAS:SCAL:POW ?'))

        if toPrint:
            print(f'Voltage: {round(voltage, 2)} V\nCurrent: {round(current, 3)} A\nPower: {round(power, 2)} W')

        return voltage, current


    def display_text(self, text: str = ".i. .i. .i. .i. .i. .i. .i. .i. .i."):
        self.rohde_schwarz.write(f'DISP:TEXT "{text}"')


if __name__ == '__main__':
    rohde_schwarz = Rohde_Schwarz()
    # rohde_schwarz.channel_config(channel=1, output=True, voltage=3, current=2)
    rohde_schwarz.voltage_current_power_measurement(channel=1, toPrint=True)