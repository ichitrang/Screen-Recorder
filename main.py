from PIL import ImageGrab
import numpy as np
import cv2
from win32api import GetSystemMetrics
import datetime
import requests

def upload_file(file_path):
    url = 'https://file.io'

    with open(file_path, 'rb') as file:
        response = requests.post(url, files={'file': file})

        if response.status_code == 200:
            response_data = response.json()
            file_link = response_data['link']
            print(f"File uploaded successfully. Link: {file_link}")
        else:
            print("Error uploading file.")

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)

time_stamp = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
file_name = f'{time_stamp}.mp4'
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
captured_Video = cv2.VideoWriter(file_name, fourcc, 20.0, (width, height))
cam = cv2.VideoCapture(0)
while True:
    img = ImageGrab.grab(bbox=(0, 0, width, height))
    img_np = np.array(img)
    img_final = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    _, frame = cam.read()
    fr_height, fr_width, _ = frame.shape
    img_final[0:fr_height, 0:fr_width, :] = frame[0:fr_height, 0:fr_width, :]
    cv2.imshow('Screen Capture', img_final)
    # cv2.imshow('cam', frame)
    captured_Video.write(img_final)
    if cv2.waitKey(10) == ord('q'):
        upload_file(file_name)
        break