import time
from oled import *
from airSensor import *
from saveData import *
from soilSensor import *
from camera import *

oled = OledClass()
airSensor = AirSensor()
data = SaveData()
camera = CameraClass()
soilSensor = SoilSensor()
counter = 0
SHUT_DOWN = 600

while counter < SHUT_DOWN:

    counter = counter + 1
    
    tmp_and_humid = airSensor.getReading()
    soil_moisture = soilSensor.getPercentageReading()
    oled.printToScreen(tmp_and_humid[0], tmp_and_humid[1], soil_moisture)
    
    # if 100 -> every 10 min a datapoint gets saved
    if counter % 100 == 0:
        data.saveDatapoint(tmp_and_humid[0], tmp_and_humid[1], soil_moisture)
    if counter == SHUT_DOWN:
        camera.takePicture()
    
    time.sleep(6.0)
    
    
