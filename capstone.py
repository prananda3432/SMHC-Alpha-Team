import cv2
import os
import time
from tensorflow.keras.models import model_from_json
import tensorflow as tf
import numpy as np
import datetime as dt

#start = time.time()
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
video_capture = cv2.VideoCapture(0)
mask_on = False

class ExpressionDetection(object):

    FACEEXPRESSION = ["Angry", "Disgust", "Fear", "Happy",
                     "Neutral", "Sad", "Shocked"]

    def __init__(self, file_json_model, file_weights_model):
        # Load model JSON and weight file
        with open(file_json_model, "r") as json_file:
            loaded_model_json = json_file.read()
            self.loaded_model = model_from_json(loaded_model_json)
        self.loaded_model.load_weights(file_weights_model)
        
    def predict_emotion(self, img):
        self.preds = self.loaded_model.predict(img)
        return ExpressionDetection.FACEEXPRESSION[np.argmax(self.preds)]

model = ExpressionDetection("model.json", "weights.h5")
t = dt.datetime.now()
interval = 10
danger_state = 0

def ambil_ss(ssan):
    cv2.imwrite('image-opencv.jpg', ssan)

while True:
    # Take frame-by-frame
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    wajah = faceCascade.detectMultiScale(gray, 1.1, 5)
    # Face box in camera
    for (x, y, w, h) in wajah:
        roi_gray = gray[y:y + h, x:x + w]
        roi_input = cv2.resize(roi_gray, (48, 48))
        
        pred = model.predict_emotion(roi_input[np.newaxis, :, :, np.newaxis])
        
        if pred == "Angry" or "Fear" or "Sad":
            danger_state += 1
        
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.putText(frame, pred, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)

    cv2.putText(frame, 'Face Detected : '+ str(len(wajah)), (30, 30), cv2.FONT_HERSHEY_SIMPLEX,  1, (0, 255, 0), 2)
    cv2.imshow('Video', frame)

    current_time = dt.datetime.now()
    delta = current_time-t
    if delta.seconds >= 10:
        ambil_ss(frame)
        t = current_time.now()

    if danger_state > 0:
        ambil_ss(frame)
        danger_state = 0

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
