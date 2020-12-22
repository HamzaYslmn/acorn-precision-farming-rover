# Simple demo of reading each analog input from the ADS1x15 and printing it to
# the screen.
# Author: Tony DiCola
# License: Public Domain
import time

# Import the ADS1x15 module.
import Adafruit_ADS1x15


# Create an ADS1115 ADC (16-bit) instance.


GAIN = 1

high_voltage_factor = (100.0 + 6.49)/6.49  # High Voltage
mid_voltage_factor = (100.0 + 10.2)/10.2  # Mid Voltage
low_voltage_factor = (44.2 + 10.2)/10.2  # Low Voltage

SYS_VOLTAGE = 3.3
MAX_VAL = 2^16


class VoltageSampler():

    def __init__(self, master_conn):
        self.adc = None
        self.master_conn = master_conn

    def read_loop(self):
        self.adc = Adafruit_ADS1x15.ADS1115(address=0x48)
        while True:
            # Read all the ADC channel values in a list.
            values = [0]*4
            for i in range(4):
                # Read the specified ADC channel using the previously set gain value.
                values[i] = self.adc.read_adc(i, gain=GAIN)
                # Note you can also pass in an optional data_rate parameter that controls
                # the ADC conversion time (in samples/second). Each chip has a different
                # set of allowed data rate values, see datasheet Table 9 config register
                # DR bit values.
                #values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
                # Each value will be a 12 or 16 bit signed integer value depending on the
                # ADC (ADS1015 = 12-bit, ADS1115 = 16-bit).
            #print(values)
            low_voltage = values[0] * low_voltage_factor * SYS_VOLTAGE/MAX_VAL * 0.001
            mid_voltage = values[1] * mid_voltage_factor * SYS_VOLTAGE/MAX_VAL * 0.001
            high_voltage = values[2] * high_voltage_factor * SYS_VOLTAGE/MAX_VAL * 0.001



            cell1 = low_voltage
            cell2 = mid_voltage - low_voltage
            cell3 = high_voltage - mid_voltage
            total = high_voltage

            input_voltages = [val * high_voltage_factor * SYS_VOLTAGE/MAX_VAL * 0.001 for val in values]


            if self.master_conn is not None:
                self.master_conn.send((cell1, cell2, cell3, total),)
            else:
                #print(input_voltages)
                print("{}, {}, {}".format(low_voltage, mid_voltage, high_voltage))
                # If run standalone, print values.
                print("{:0.2f} V | {:0.2f} V | {:0.2f} V | total: {:0.2f} V".format(cell1, cell2, cell3, total))
                print(' Input Voltage Values: | {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*input_voltages))
                #print(' Raw Values: | {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
            # Pause for half a second.
            time.sleep(1)

def sampler_loop(master_conn):
    sampler = VoltageSampler(master_conn)
    sampler.read_loop()

if __name__=="__main__":
    sampler_loop(None)