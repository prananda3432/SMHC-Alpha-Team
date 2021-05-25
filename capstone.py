import cv2
import os
import time
from tensorflow.keras.models import model_from_json
import tensorflow as tf
import numpy as np

#start = time.time()
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
video_capture = cv2.VideoCapture(0)
mask_on = False

class DeteksiEkspresi(object):

    EKSPRESIWAJAH = ["Angry", "Disgust", "Fear", "Happy",
                     "Neutral", "Sad", "Shocked"]

    def __init__(self, file_json_model, file_weights_model):
        # memuat model json dan weight
        with open(file_json_model, "r") as json_file:
            loaded_model_json = json_file.read()
            self.loaded_model = model_from_json(loaded_model_json)
        self.loaded_model.load_weights(file_weights_model)
        
    def predict_emotion(self, img):
        self.preds = self.loaded_model.predict(img)
        return DeteksiEkspresi.EKSPRESIWAJAH[np.argmax(self.preds)]

model = DeteksiEkspresi("model.json", "weights.h5")

while True:
    # ambil frame-by-frame
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    wajah = faceCascade.detectMultiScale(gray, 1.1, 5)

    # gambar kotak di wajah
    for (x, y, w, h) in wajah:
        roi_gray = gray[y:y + h, x:x + w]
        roi_input = cv2.resize(roi_gray, (48, 48))
        
        pred = model.predict_emotion(roi_input[np.newaxis, :, :, np.newaxis])
        
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.putText(frame, pred, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)

    cv2.putText(frame, 'Face Detected : '+ str(len(wajah)), (30, 30), cv2.FONT_HERSHEY_SIMPLEX,  1, (0, 255, 0), 2)
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
