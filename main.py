import time
from oled import *
from airSensor import *
from saveData import *
from soilSensor import *
from camera import *

# Change here to the number of connected soil sensors
number_of_soil_sensors = 3;

oled = OledClass(number_of_soil_sensors)
airSensor = AirSensor()
data = SaveData(number_of_soil_sensors)
camera = CameraClass()
soilSensor = SoilSensor(number_of_soil_sensors)
counter = 0
soil_moisture = [None] * number_of_soil_sensors
SHUT_DOWN = 600


while counter < SHUT_DOWN:

    counter = counter + 1
    
    tmp_and_humid = airSensor.getReading()
    for x in range(number_of_soil_sensors):
        soil_moisture[x] = soilSensor.getPercentageReading(x)
    oled.printToScreen(tmp_and_humid[0], tmp_and_humid[1], soil_moisture)
    
    # if 100 -> every 10 min a datapoint gets saved
    if counter % 100 == 0:
        data.saveDatapoint(tmp_and_humid[0], tmp_and_humid[1], soil_moisture)
    if counter == SHUT_DOWN:
        camera.takePicture()
    
    time.sleep(6.0)
    
    
