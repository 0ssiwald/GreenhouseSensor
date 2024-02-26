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
            return round(sensor.temperature, 2), round(sensor.relative_humidity, 2)
        else:
            return [0, 0]
        


if __name__ == "__main__":
    sensor = AirSensor()
    print(sensor.getReading())
