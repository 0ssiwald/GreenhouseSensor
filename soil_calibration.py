import time
import json
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create input on channel 0 to 2
chan = [AnalogIn(ads, ADS.P0), AnalogIn(ads, ADS.P1), AnalogIn(ads, ADS.P2)]

def calibrate_sensor(sensor_index):
    full_saturation_sum = 0
    zero_saturation_sum = 0

    print(f"\nCalibrating Capacitive Sensor {sensor_index + 1}")
    
    baseline_check = input("\nIs it Dry? (enter 'y' to proceed): ")
    if baseline_check == 'y':
        for _ in range(10):
            value = chan[sensor_index].value
            full_saturation_sum += value
            print(f"Raw: {value}\tVoltage: {chan[sensor_index].voltage:.3f}")
            time.sleep(0.5)

    water_check = input("\nIs it in Water? (enter 'y' to proceed): ")
    if water_check == 'y':
        for _ in range(10):
            value = chan[sensor_index].value
            zero_saturation_sum += value
            print(f"Raw: {value}\tVoltage: {chan[sensor_index].voltage:.3f}")
            time.sleep(0.5)

    full_saturation_mean = full_saturation_sum / 10
    zero_saturation_mean = zero_saturation_sum / 10

    return full_saturation_mean, zero_saturation_mean

num_of_sensors = int(input("How many sensors are connected (enter '1', '2', or '3'): "))

calibration_data = {}

for x in range(num_of_sensors):
    full_saturation_mean, zero_saturation_mean = calibrate_sensor(x)
    calibration_data[f"Sensor_{x + 1}"] = {
        "full_saturation": full_saturation_mean,
        "zero_saturation": zero_saturation_mean
    }

with open('config.json', 'w') as outfile:
    json.dump(calibration_data, outfile, indent=4)

print('\nCalibration Complete')
