import time
from oled import OledClass
from airSensor import AirSensor
from saveData import SaveData
from soilSensor import SoilSensor
from camera import CameraClass



# Change here to the number of connected soil sensors (1-3)
NUMBER_OF_SOIL_SENSORS = 3;
# Change here to change how long the program is running 
# there is a bug were the pi crashes if the program runs for to long 
SHUT_DOWN = 600
# Defines how often a datapoint is saved in combination with SLEEP_TIME
# if 100 with SLEEP_TIME = 6.0 -> every 10 min a datapoint gets saved
SAVE_DATAPOINT = 300
# Change here how many sec the program sleeps
SLEEP_TIME = 5.0
# If the flusk webserver is runnig
IS_WEBSERVER_RUNNING = True

oled = OledClass(NUMBER_OF_SOIL_SENSORS)
airSensor = AirSensor()
data = SaveData("data.csv", NUMBER_OF_SOIL_SENSORS)
soilSensor = SoilSensor(NUMBER_OF_SOIL_SENSORS)
counter = 0
soil_moisture = [None] * NUMBER_OF_SOIL_SENSORS

while counter < SHUT_DOWN:
    counter = counter + 1
    tmp_and_humid = airSensor.getReading()
    
    for x in range(NUMBER_OF_SOIL_SENSORS):
        soil_moisture[x] = soilSensor.getPercentageReading(x)
    oled.printToScreen(tmp_and_humid[0], tmp_and_humid[1], soil_moisture)
    
    if counter % SAVE_DATAPOINT == 0:
        data.saveDatapoint(tmp_and_humid[0], tmp_and_humid[1], soil_moisture)
        
    if counter == SHUT_DOWN:
     # camera and plotter are instanciated and deleted in loop to prevent leaks
        if IS_WEBSERVER_RUNNING:
            plotter = CreatePlots("data.csv")
            plotter.makeHumidAndTmpPlot("Webserver/static/humid_and_tmp.jpg")
            plotter.makeSoilMoisturePlot("Webserver/static/soil_moisture.jpg", NUMBER_OF_SOIL_SENSORS)
            del plotter
        camera = CameraClass(IS_WEBSERVER_RUNNING) 
        camera.takePictureAndDeleteIfBlack()
        del camera
        
    time.sleep(SLEEP_TIME)
    
del oled

    
    
