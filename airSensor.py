# https://github.com/adafruit/Adafruit_CircuitPython_AHTx0

import board
import adafruit_ahtx0

class AirSensor():
    def __init__(self):
        # Create sensor object, communicating over the board's default I2C bus
        self.i2c = board.I2C()  # uses board.SCL and board.SDA

    def getReading(self):
        sensor = adafruit_ahtx0.AHTx0(self.i2c)
        if sensor.temperature is not None and sensor.relative_humidity is not None:
            return round(sensor.temperature, 1), int(round(sensor.relative_humidity, 0))
        else:
            return [0, 0]
        
    def calcVpd(self, temperature, humidity):
        vp_sat = (610.7 * 10 ** ((7.5*temperature)/(237.3+temperature)))/1000
        v_pair = vp_sat * (humidity/100)
        vpd = vp_sat - v_pair
        return round(vpd, 2)
    
    def getTempHumidVpd(self):
        temperature, humidity = self.getReading()
        vpd = self.calcVpd(temperature, humidity)
        return temperature, humidity, vpd


if __name__ == "__main__":
    sensor = AirSensor()
    print(sensor.getReading())
