import time
from board import SCL, SDA
import busio
import os
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

class OledClass():

    # Create the I2C interface.
    i2c = busio.I2C(SCL, SDA)

    # Create the SSD1306 OLED class.
    # The first two parameters are the pixel width and pixel height.  Change these
    # to the right size for your display!
    disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

    # Clear display.
    disp.fill(0)
    disp.show()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new("1", (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    bottom = height - padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0
    # the ttf File needs to be in the same folder and the number is the size
    font_size = 20
    
    #This is to avoid any path-related issues
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(script_dir, 'PixelOperator.ttf')
    font = ImageFont.truetype(font_path, font_size)

    def printToScreen(self, temperature, humidity, moisture):
        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        
        # So that the Display blinks to signal that the programm is still running
        time.sleep(0.1)
        self.disp.image(self.image)
        self.disp.show()
        
        # Write four lines of text.
        self.draw.text((self.x, self.top),  "Soil: " + str(moisture) + "%", font=self.font, fill=255)
        self.draw.text((self.x, self.top+self.font_size),  "Tmp: "  + str(temperature) + " °C", font=self.font, fill=255)
        self.draw.text((self.x, self.top+2*self.font_size), "Humid: " + str(humidity) + "%", font=self.font, fill=255)
        
        # Display image.
        self.disp.image(self.image)
        self.disp.show()
     
    # destructor to make the display black if the process stops
    def __del__(self):
        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        self.disp.image(self.image)
        self.disp.show()
        