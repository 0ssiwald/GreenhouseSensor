import pandas as pd
import matplotlib.pyplot as plt

class CreatePlots:
    def __init__(self, data_file):
        self.data = pd.read_csv(data_file, parse_dates=['datetime'], dayfirst=True)

    def makeHumidAndTmpPlot(self, output_file):
        # Convert the columns to numpy arrays
        datetime = self.data["datetime"].values
        temperature = self.data[" temperature[*C]"].values
        humidity = self.data[" humidity[%]"].values
        # Create a figure and plot the data
        plt.figure(figsize=(10, 6))
        # Temperature plot
        ax1 = plt.gca()
        ax1.plot(datetime, temperature, label="Temperature", marker='o', color='tab:red')
        ax1.set_xlabel("Date/Time")
        ax1.set_ylabel("Temperature [°C]", color='tab:red')
        ax1.tick_params(axis='y', labelcolor='tab:red')
        # Secondary y-axis for Humidity
        ax2 = ax1.twinx()
        ax2.plot(datetime, humidity, label="Humidity", marker='o', color='tab:blue')
        ax2.set_ylabel("Humidity [%]", color='tab:blue')
        ax2.tick_params(axis='y', labelcolor='tab:blue')
        # Title and legend
        plt.title("Temperature and Humidity Over Time")
        plt.xticks(rotation=45)
        plt.grid()
        plt.tight_layout()
        # Save the plot to the specified output file
        plt.savefig(output_file, dpi=300)
        plt.close()  # Close the figure
        
    def makeSoilMoisturePlot(self, output_file, number_of_soil_sensors):
        datetime = self.data["datetime"].values
        soil1 = self.data[" soil_s1[%]"].values
        if number_of_soil_sensors > 1:
            soil2 = self.data[" soil_s2[%]"].values
        if number_of_soil_sensors > 2:
            soil3 = self.data[" soil_s3[%]"].values
        
        # Create a figure and plot the data
        plt.figure(figsize=(10, 6))
        
        plt.plot(datetime, soil1, label="SoilSensor 1", marker='o')
        if number_of_soil_sensors > 1:
            plt.plot(datetime, soil2, label="SoilSensor 2", marker='o')
        if number_of_soil_sensors > 2:
            plt.plot(datetime, soil3, label="SoilSensor 3", marker='o')
        plt.xlabel("Date/Time")
        plt.ylabel("Soil Moisture [%]")
        # Title and legend
        plt.title("Soil Moisture Over Time")
        plt.grid()
        if number_of_soil_sensors > 1:
            plt.legend()
        plt.tight_layout()
        # Save the plot to the specified output file
        plt.savefig(output_file, dpi=300)
        plt.close()  # Close the figure
        
    def __del__(self):
        del self.data  # Manually delete the DataFrame

# Example usage:
if __name__ == "__main__":
    plotter = CreatePlots("logs/sensor_data.csv")
    plotter.makeHumidAndTmpPlot("test1.jpg")
    plotter.makeSoilMoisturePlot("test2.jpg", 3)
