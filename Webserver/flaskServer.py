from flask import Flask, render_template
from collections import deque
import csv
import os


app = Flask(__name__)


@app.route('/')
def display_data():
    data = []
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    data_path = os.path.join(data_dir, "logs/sensor_data.csv")

    with open(data_path, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        last_10_rows = deque(maxlen=10)  # Create a deque with a maximum size of 10
        for row in csvreader:
            last_10_rows.appendleft(row) # Append to the left to reverse the order
        data = list(last_10_rows)

    newest_image = "newest_image.jpg"
    humid_and_tmp = "humid_and_tmp.jpg"
    soil_moisture = "soil_moisture.jpg"
    vpd = "vpd.jpg"
    
    return render_template('index.html', data=data, newest_image=newest_image, humid_and_tmp=humid_and_tmp, vpd=vpd, soil_moisture=soil_moisture)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


'''
def get_newest_image():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pictures_dir = os.path.join(script_dir, "static")
    image_files = [f for f in os.listdir(pictures_dir) if f.endswith('.jpg')]
    if image_files:
        newest_image = max(image_files, key=lambda f: os.path.getctime(os.path.join(pictures_dir, f)))
        return newest_image
    else:
        return None
'''   