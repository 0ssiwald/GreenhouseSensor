from datetime import datetime
import os

class SaveData:
    
    def __init__(self, number_of_soilsensors):
        self.number_of_soilsensors = number_of_soilsensors
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir, "data.csv")
    isExisting = os.path.exists(path)
    csvFile = open(path, "a")
    if isExisting == False:
        csvFile.write("datetime, temperature[*C], humidity[%], soil_s1[%], soil_s2[%], soil_s3[%] \n")
    csvFile.close()
    
    def saveDatapoint(self, temperature, humidity, moisture):
    
        if self.number_of_soilsensors < 1 or self.number_of_soilsensors > 3:
            raise ValueError("Invalid sensor index")
            
        self.csvFile = open(self.path, "a")
        self.csvFile.write(datetime.today().strftime('%d/%m/%Y %H:%M:%S')+", ")
        self.csvFile.write('{0:0.1f}, {1:0.1f}, '.format(temperature, humidity))
        if self.number_of_soilsensors == 1 :
            self.csvFile.write('{2:0.1f}, 0.0, 0.0'.format(moisture[0]))
        elif self.number_of_soilsensors == 2 :
            self.csvFile.write('{2:0.1f}, {2:0.1f}, 0.0'.format(moisture[0], moisture[1]))
        elif self.number_of_soilsensors == 3 :
            self.csvFile.write('{2:0.1f}, {2:0.1f}, {2:0.1f}'.format(moisture[0], moisture[1], moisture[2]))
        self.csvFile.write('\n')
        self.csvFile.close()
            