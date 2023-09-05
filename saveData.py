from datetime import datetime
import os

class SaveData:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir, "data.csv")
    isExisting = os.path.exists(path)
    csvFile = open(path, "a")
    if isExisting == False:
        csvFile.write("datetime, temperature[*C], humidity[%], soil moisture[%] \n")
    csvFile.close()
    
    def saveDatapoint(self, temperature, humidity, moisture):
        self.csvFile = open(self.path, "a")
        self.csvFile.write(datetime.today().strftime('%d/%m/%Y %H:%M:%S')+", ")
        self.csvFile.write('{0:0.1f}, {1:0.1f}, {2:0.1f}'.format(temperature, humidity, moisture))
        self.csvFile.write('\n')
        self.csvFile.close()
            