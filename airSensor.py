import Adafruit_DHT

class AirSensor():
    # change here from DHT11 to 22 if the senor changes
    sensor = Adafruit_DHT.DHT22

    # connected to GPIO18.
    pin = 18

    def getReading(self):
        # Try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)

        # Note that sometimes you won't get a reading and
        # the results will be null (because Linux can't
        # guarantee the timing of calls to read the sensor).
        # If this happens try again!
        if humidity is not None and temperature is not None:
            return round(temperature, 2), round(humidity, 2)
        else:
            return [0, 0]
