import time
import copy
from oled import OledClass
from airSensor import AirSensor
from saveData import SaveData
from soilSensor import SoilSensor
from camera import CameraClass
from wateringPlants import wateringPlants
from dataGraphs import CreatePlots



# Change here to the number of connected soil sensors (1-3)
NUMBER_OF_SOIL_SENSORS = 1
# Change here to change how long the program is running 
# there is a bug were the pi crashes if the program runs for to long 
SHUT_DOWN = 1
# Defines how often a datapoint is saved in combination with SLEEP_TIME
# if 100 with SLEEP_TIME = 6.0 -> every 10 min a datapoint gets saved
SAVE_DATAPOINT = 100
# Change here how many sec the program sleeps
SLEEP_TIME = 6
# If the flusk webserver is runnig
IS_WEBSERVER_RUNNING = True
# Set true if the Watering system is connected to the pi
IS_WATERING_SYSTEM_ACTIVE = False

oled = OledClass(NUMBER_OF_SOIL_SENSORS)
airSensor = AirSensor()
data = SaveData("logs/sensor_data.csv", NUMBER_OF_SOIL_SENSORS)
soilSensor = SoilSensor(NUMBER_OF_SOIL_SENSORS)
waterPlants = wateringPlants("logs/watering_events.csv", NUMBER_OF_SOIL_SENSORS)
plotter = CreatePlots("logs/sensor_data.csv")
counter = 0
soil_moisture = [None] * NUMBER_OF_SOIL_SENSORS
previous_soil_moisture = [None] * NUMBER_OF_SOIL_SENSORS

while True:#counter < SHUT_DOWN:
    counter = counter + 1
    temperature, humidity, vpd = airSensor.getTempHumidVpd()
    previous_soil_moisture = copy.deepcopy(soil_moisture) #Copy is needed so that old_soil_moisture dont get updated when soil_moisture changes
    for x in range(NUMBER_OF_SOIL_SENSORS):
        soil_moisture[x] = soilSensor.getPercentageReading(x)
    waterPlants.testForManualWatering(previous_soil_moisture, soil_moisture)
    oled.printToScreen(temperature, humidity, vpd, soil_moisture)
    
    if counter % SAVE_DATAPOINT == 0:
        data.saveDatapoint(temperature, humidity, vpd, soil_moisture)
        
    if counter == SHUT_DOWN:
     # camera and plotter are instanciated and deleted in loop to prevent leaks
        if IS_WEBSERVER_RUNNING:
            plotter.makeHumidAndTmpPlot("Webserver/static/humid_and_tmp.jpg")
            plotter.makeVpdPlot("Webserver/static/vpd.jpg")
            plotter.makeSoilMoisturePlot("Webserver/static/soil_moisture.jpg", NUMBER_OF_SOIL_SENSORS)

       # if IS_WATERING_SYSTEM_ACTIVE:
         #   wateringPlants.testForWatering()
        camera = CameraClass(IS_WEBSERVER_RUNNING) 
        camera.takePictureAndDeleteIfBlack()
        del camera
        counter = 0  
        
    time.sleep(SLEEP_TIME)
    
del oled
del plotter

    
    
