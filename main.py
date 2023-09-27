import time
from oled import OledClass
from airSensor import AirSensor
from saveData import SaveData
from soilSensor import SoilSensor
from camera import CameraClass

# Change here to the number of connected soil sensors (1-3)
number_of_soil_sensors = 3;
# Change here to change how long the program is running 
# there is a bug were the pi crashes if the program runs for to long 
SHUT_DOWN = 600
# Defines how often a datapoint is saved in combination with SLEEP_TIME
# if 100 with SLEEP_TIME = 6.0 -> every 10 min a datapoint gets saved
SAVE_DATAPOINT = 100
# Change here how many sec the program sleeps
SLEEP_TIME = 5.0

oled = OledClass(number_of_soil_sensors)
airSensor = AirSensor()
data = SaveData(number_of_soil_sensors)
soilSensor = SoilSensor(number_of_soil_sensors)
counter = 0
soil_moisture = [None] * number_of_soil_sensors

while counter < SHUT_DOWN:
    counter = counter + 1
    tmp_and_humid = airSensor.getReading()
    for x in range(number_of_soil_sensors):
        soil_moisture[x] = soilSensor.getPercentageReading(x)
    oled.printToScreen(tmp_and_humid[0], tmp_and_humid[1], soil_moisture)
    if counter % SAVE_DATAPOINT == 0:
        data.saveDatapoint(tmp_and_humid[0], tmp_and_humid[1], soil_moisture)
    if counter == SHUT_DOWN:
        # camera is instanciated and deleted in loop to prevent leaks
        camera = CameraClass() 
        camera.takePictureAndDeleteIfBlack()
        del camera
        
    time.sleep(SLEEP_TIME)
    
del oled

    
    
