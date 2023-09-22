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
    i2c = busio.I2C(board.SCL, board.SDA)
 
    # Create an ADS1115 object
    ads = ADS.ADS1115(i2c)
 
    # Define the analog input channels
    channels = [AnalogIn(ads, ADS.P0), AnalogIn(ads, ADS.P1), AnalogIn(ads, ADS.P2)]
    
    #opens json to read max and min values
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(script_dir, "config.json")
    with open(font_path) as json_data_file:
        config_data = json.load(json_data_file)
    
    
    
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
    
    
#    def getPercentageReading(self):
 #       raw_value = self.channel.value
  #      if raw_value is not None:
   #         percentage_value = abs((raw_value-self.config_data["zero_saturation"])/(self.config_data["full_saturation"]-self.config_data["zero_saturation"]))*100
    #        return round(percentage_value, 2)
     #   else:
      #      return 0
    
    