from datetime import datetime
import os

class SaveData:
    
    def __init__(self, data_file, number_of_soilsensors):
        self.number_of_soilsensors = number_of_soilsensors
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.path = os.path.join(self.script_dir, data_file)
        self.isExisting = os.path.exists(self.path)
        self.csvFile = open(self.path, "a")
        if self.isExisting == False:
            self.csvFile.write("datetime, temperature[*C], humidity[%], vpd[kPa], soil_s1[%], soil_s2[%], soil_s3[%]\n")
        self.csvFile.close()
    
    def saveDatapoint(self, temperature, humidity, vpd, moisture):
    
        if self.number_of_soilsensors < 1 or self.number_of_soilsensors > 3:
            raise ValueError("Invalid sensor index")
            
        self.csvFile = open(self.path, "a")
        self.csvFile.write(datetime.today().strftime('%d/%m/%Y %H:%M:%S')+", ")
        self.csvFile.write('{0:0.1f}, {1}, {2:0.2f}, '.format(temperature, humidity, vpd))
        if self.number_of_soilsensors == 1 :
            self.csvFile.write('{0:0.1f}, 0.0, 0.0'.format(moisture[0]))
        elif self.number_of_soilsensors == 2 :
            self.csvFile.write('{0:0.1f}, {1:0.1f}, 0.0'.format(moisture[0], moisture[1]))
        elif self.number_of_soilsensors == 3 :
            self.csvFile.write('{0:0.1f}, {1:0.1f}, {2:0.1f}'.format(moisture[0], moisture[1], moisture[2]))
        self.csvFile.write('\n')
        self.csvFile.close()
            