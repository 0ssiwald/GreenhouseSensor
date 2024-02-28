import os
from datetime import datetime
from PIL import Image
import random
import subprocess

class CameraClass():

    def __init__(self, is_webserver_running, in_debug_mode=False):
        self.is_webserver_running = is_webserver_running
        self.in_debug_mode = in_debug_mode
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

    def takePicture(self):
        image_filename = os.path.join(self.script_dir, 'pictures', datetime.now().strftime('%Y_%m_%d__%H_%M') + '.jpg')
        # Use libcamera-still to capture an image with higher JPEG quality and resolution
        cmd = ['libcamera-jpeg', '-o', image_filename, '--nopreview'] #'--vflip'
        subprocess.run(cmd, check=True)
        return image_filename

    def isMostlyBlack(self, image_path, threshold=30, sample_size=1000): # Adjust the threshold for the black value 
        # Load the image using Pillow
        img = Image.open(image_path)
        img_data = img.getdata()
        black_count = 0

        # Randomly sample a subset of pixels
        sampled_pixels = random.sample(list(img_data), sample_size)

        for pixel in sampled_pixels:
            r, g, b = pixel
            if r < threshold and g < threshold and b < threshold:
                black_count += 1

        if self.in_debug_mode:
            print("Blackcount: ", black_count)
            print("Sample size: ", sample_size)
            print(black_count / sample_size)

        return (black_count / sample_size) > 0.9  # Adjust the threshold as needed
    
    def saveSymlinkToStaticFolder(self, last_image):
        static_image_path = os.path.join(self.script_dir, "Webserver/static/newest_image.jpg")
        last_image_path = last_image
        
        if os.path.exists(static_image_path):
            os.remove(static_image_path)
        os.symlink(last_image_path, static_image_path)

    def takePictureAndDeleteIfBlack(self):
        last_image = self.takePicture()
        if self.isMostlyBlack(last_image):
            os.remove(last_image)
        else:
            if self.is_webserver_running:
                self.saveSymlinkToStaticFolder(last_image) # for the web server


if __name__ =="__main__":
    camera = CameraClass(False, True)
    camera.takePictureAndDeleteIfBlack()

'''
from picamera import PiCamera
from datetime import datetime
import os
from PIL import Image
import random

class CameraClass():

    def __init__(self, is_webserver_running):
        self.is_webserver_running = is_webserver_running
        self.camera = PiCamera()
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
    
    def takePicture(self):
        self.camera.start_preview()
        self.camera.resolution = (1920, 1080) # biggest: (2592, 1944) but this creates memory issues with pi zero
        image_filename = self.script_dir + '/pictures/' + datetime.today().strftime('%Y_%m_%d__%H_%M') + '.jpg'
        self.camera.capture(image_filename)
        self.camera.stop_preview()
        return image_filename

    def isMostlyBlack(self, image_path, threshold=10, sample_size=1000):
        # Load the image using Pillow
        img = Image.open(image_path)
        img_data = img.getdata()
        black_count = 0

        # Randomly sample a subset of pixels
        sampled_pixels = random.sample(list(img_data), sample_size)

        for pixel in sampled_pixels:
            r, g, b = pixel
            if r < threshold and g < threshold and b < threshold:
                black_count += 1

        return (black_count / sample_size) > 0.9  # Adjust the threshold as needed
    
    def saveSymlinkToStaticFolder(self, last_image):
        static_image_path = os.path.join(self.script_dir, "Webserver/static/newest_image.jpg")
        pictures_path = os.path.join(self.script_dir, "/pictures/")
        last_image_path = os.path.join(pictures_path, last_image)
        
        if os.path.exists(static_image_path):
            os.remove(os.path.join(static_image_path))
        os.symlink(last_image_path, static_image_path)
        
        
    def takePictureAndDeleteIfBlack(self):
        last_image = self.takePicture()
        if self.isMostlyBlack(last_image):
            os.remove(last_image)
        else:
            if self.is_webserver_running:
                self.saveSymlinkToStaticFolder(last_image) # for the web server
            
    def __del__(self):
        self.camera.close()

'''