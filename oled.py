import time
from board import SCL, SDA
import busio
import os
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

class OledClass:
    # Constants
    WIDTH = 128
    HEIGHT = 64
    PADDING = -4
    FONT_SIZE = 19

    def __init__(self, number_of_soilsensors):
        self.number_of_soilsensors = number_of_soilsensors
        self.i2c = busio.I2C(SCL, SDA)
        self.disp = adafruit_ssd1306.SSD1306_I2C(self.WIDTH, self.HEIGHT, self.i2c)
        self.image = Image.new("1", (self.WIDTH, self.HEIGHT))
        self.draw = ImageDraw.Draw(self.image)
        self.font = self.load_font()

    def load_font(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(script_dir, 'PixelOperator.ttf')
        return ImageFont.truetype(font_path, self.FONT_SIZE)

    def clear_display(self):
        self.draw.rectangle((0, 0, self.WIDTH, self.HEIGHT), outline=0, fill=0)
        self.disp.image(self.image)
        self.disp.show()

    def printToScreen(self, temperature, humidity, vpd, moisture):
        self.clear_display()

        if self.number_of_soilsensors < 1 or self.number_of_soilsensors > 3:
            raise ValueError("Invalid sensor index")
            
        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.WIDTH, self.HEIGHT), outline=0, fill=0)
        
        # So that the Display blinks to signal that the programm is still running
        time.sleep(0.1)
        self.disp.image(self.image)
        self.disp.show()
        
        if self.number_of_soilsensors == 1 :
            self.draw.text((0, self.PADDING),  "Soil: " + str(moisture[0]) + "%", font=self.font, fill=255)
        elif self.number_of_soilsensors == 2 :
            self.draw.text((0, self.PADDING),  "Soil: " + str(moisture[0]) + "% " + str(moisture[1]) + "%", font=self.font, fill=255)
        elif self.number_of_soilsensors == 3 :
            self.draw.text((0, self.PADDING),  "Soil: " + str(moisture[0]) + " " + str(moisture[1]) + " " + str(moisture[2]) + "%", font=self.font, fill=255)
        self.draw.text((0, self.PADDING+self.FONT_SIZE),  "T: "  + str(temperature) + " °C" + " RH: " + str(humidity) + "%", font=self.font, fill=255)
        self.draw.text((0, self.PADDING+2*self.FONT_SIZE), "VPD: " + str(vpd) + " kPa", font=self.font, fill=255)
        
        # Display image.
        self.disp.image(self.image)
        self.disp.show()
     
    # destructor to make the display black 
    def __del__(self):
        self.clear_display()
