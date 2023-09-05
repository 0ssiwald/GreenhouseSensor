import os
import board
import busio
import json
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time

class SoilSensor():
    # Initialize the I2C interface
    i2c = busio.I2C(board.SCL, board.SDA)
 
    # Create an ADS1115 object
    ads = ADS.ADS1115(i2c)
 
    # Define the analog input channels
    channel = AnalogIn(ads, ADS.P0)
    
    #opens json to read max and min values
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(script_dir, "cap_config.json")
    with open(font_path) as json_data_file:
        config_data = json.load(json_data_file)
    
    def getRawReading(self):
        return self.channel.value
    
    def getPercentageReading(self):
        raw_value = self.channel.value
        if raw_value is not None:
            percentage_value = abs((raw_value-self.config_data["zero_saturation"])/(self.config_data["full_saturation"]-self.config_data["zero_saturation"]))*100
            return round(percentage_value, 2)
        else:
            return 0
    