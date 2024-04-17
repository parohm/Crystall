class Agilent_34980a(object):
    def __init__(self):
        import pyvisa
        self.instruments = pyvisa.ResourceManager()
        self.agilent_34890a = self.instruments.open_resource('USB0::0x0957::0x0507::MY44002633::INSTR')



    def temperature_measurement(self,
                                channel: int,
                                console_output: bool = False):

        self.agilent_34890a.write(f'MEAS:TEMPerature? THERmistor, 10000, (@{channel},)')

        temperature = float(self.agilent_34890a.read())
        if console_output:
            print(f'CH{channel} temperature: {round(temperature, 2)} C')

        return temperature

    def resistance_measurement(self,
                               channel: int,
                               console_output: bool = False):

        output_message = f'MEAS:RESistance? (@{channel})'

        self.agilent_34890a.write(output_message)

        resistance = float(self.agilent_34890a.read())
        if console_output:
            print(f'CH{channel} resistance: {round(resistance, 5)} Ohm')

        return resistance

    def voltage_measurement(self,
                            channel: int,
                            console_output: bool = False,
                            current_type='DC'):

        output_message = f'MEAS:VOLT:{current_type}? (@{channel})'

        self.agilent_34890a.write(output_message)

        voltage = float(self.agilent_34890a.read())
        if console_output:
            print(f'CH{channel} voltage: {round(voltage, 5)} V')

        return voltage

    def current_measurement(self,
                            channel: int,
                            console_output: bool = False,
                            current_type='DC'):
        """
        channel: only 1041...1044
        """
        output_message = f'MEAS:CURR:{current_type}? (@{channel},)'
        self.agilent_34890a.write(output_message)

        current = float(self.agilent_34890a.read())
        if console_output:
            print(f'CH{channel} current: {round(current * 10 ** 3, 5)} mA')

        return float(current)

    def open_channel(self,
                     channel: int or str):
        return self.agilent_34890a.write(f'ROUT:OPEN (@{channel})')

    def close_channel(self,
                      channel: int or str):
        return self.agilent_34890a.write(f'ROUT:CLOS (@{channel})')

if __name__ == '__main__':
    agilent_34980a = Agilent_34980a()
    agilent_34980a.close_channel(channel=1001)
