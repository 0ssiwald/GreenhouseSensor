from datetime import datetime
import os


class wateringPlants:

    def __init__(self, water_log_file, number_of_soilsensors):
        self.number_of_soilsensors = number_of_soilsensors
        self.water_log_file = water_log_file
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.path = os.path.join(self.script_dir, self.water_log_file)
        self.isExisting = os.path.exists(self.path)
        self.csvFile = open(self.path, "a")
        if self.isExisting == False:
            self.csvFile.write("datetime, plant number, previous moisture level[%], new moisture level[%]\n")
        self.csvFile.close()

    def saveWateringEvent(self, plant_number, previous_moisture_level, new_moisture_level):
        self.csvFile = open(self.path, "a")
        self.csvFile.write(datetime.today().strftime('%d/%m/%Y %H:%M:%S')+", ")
        self.csvFile.write("{}, {}, {} \n".format(plant_number, previous_moisture_level, new_moisture_level))
        #self.csvFile.write('\n')
        self.csvFile.close()

    def testForManualWatering(self, previous_moisture_level, new_moisture_level):
        diffrence_threshold = 5 # Diffrence in moisture that trigges the logging of a manual watering
        for x in range(self.number_of_soilsensors):
            if previous_moisture_level[x] is not None and new_moisture_level[x] is not None:
                if new_moisture_level[x] - previous_moisture_level[x] >= diffrence_threshold:
                    self.saveWateringEvent(x+1, previous_moisture_level[x], new_moisture_level[x])



