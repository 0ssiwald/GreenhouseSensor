from picamera import PiCamera
from datetime import datetime
import os

class CameraClass():
    camera = PiCamera()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    def takePicture(self):
        self.camera.start_preview()
        self.camera.resolution = (2592, 1944)
        self.camera.capture(self.script_dir + '/pictures/' + datetime.today().strftime('%Y_%m_%d__%H_%M')+'.jpg')
        self.camera.stop_preview()