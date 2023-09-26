import os
import board
import busio
import json
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time

class SoilSensor:

    def __init__(self, number_of_soilsensors):
        self.number_of_soilsensors = number_of_soilsensors
        # Initialize the I2C interface
        self.i2c = busio.I2C(board.SCL, board.SDA)
        # Create an ADS1115 object
        self.ads = ADS.ADS1115(self.i2c)
        # Define the analog input channels
        self.channels = [AnalogIn(self.ads, ADS.P0), AnalogIn(self.ads, ADS.P1), AnalogIn(self.ads, ADS.P2)]
    
        #opens json to read max and min values
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.font_path = os.path.join(self.script_dir, "config.json")
        with open(self.font_path) as json_data_file:
            self.config_data = json.load(json_data_file)
    
    
    
    def getPercentageReading(self, sensor_index):
        if sensor_index < 0 or sensor_index >= self.number_of_soilsensors:
            raise ValueError("Invalid sensor index")

        raw_value = self.channels[sensor_index].value
        if raw_value is not None:
            full_saturation = self.config_data[f"Sensor_{sensor_index + 1}"]["full_saturation"]
            zero_saturation = self.config_data[f"Sensor_{sensor_index + 1}"]["zero_saturation"]

            percentage_value = abs((raw_value - zero_saturation) / (full_saturation - zero_saturation)) * 100
            return int(round(percentage_value, 0))
        else:
            return 0
    
    
    