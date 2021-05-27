import cv2
import os
import time
import pyrebase
import tensorflow as tf
import numpy as np
import datetime as dt
import FCMManager as fcm
from tensorflow.keras.models import model_from_json


#Firebase config
firebaseConfig = {
    "apiKey": "AIzaSyDfzAPahVi11ijBB7_KiD53s3K2_UF4uBo",
    "authDomain": "logical-seat-314215.firebaseapp.com",
    "databaseURL": "https://logical-seat-314215-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "logical-seat-314215",
    "storageBucket": "logical-seat-314215.appspot.com",
    "messagingSenderId": "390165501434",
    "appId": "1:390165501434:web:8103c9767e82aedd92c043",
    "measurementId": "G-PLXNTPP82Y"
}

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()
smhc_database = firebase.database()
upload_image_normal = "image-opencv-normal.jpg"
upload_image_danger = "image-opencv-danger.jpg"

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
video_capture = cv2.VideoCapture(0)
mask_on = False

# Firebase admin account
auth = firebase.auth()
email = "<email address>"
password = "<email password>"
user = auth.sign_in_with_email_and_password(email, password)

FCM_tokens = [""]

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
interval = 5
danger_state = 0

def take_capture_1(ssan):
    cv2.imwrite(upload_image_normal, ssan)
    storage.child(upload_image_normal).put(upload_image_normal)
    time.sleep(5)
    storage.child(prove_image_normal).put(upload_image_normal)
    #Push and update the database normal
    #"""
    image_url = storage.child(upload_image_normal).get_url(user['idToken'])
    data_database={"Status": "Normal", "Date": date_string, "Time": time_string, "image_url": image_url}
    smhc_database.child("OpenCV-Normal").set(data_database)
    print ("Success Push to Database OpenCV-Normal")
    #"""

def take_capture_2(ssan):
    cv2.imwrite('image-opencv-danger.jpg', ssan)
    storage.child(upload_image_danger).put(upload_image_danger)
    storage.child(prove_image_danger).put(upload_image_danger)
    time.sleep(5)
    #Push and update the database normal
    #"""
    image_url = storage.child(upload_image_danger).get_url(user['idToken'])
    data_database={"Status": "Danger", "Date": date_string, "Time": time_string, "image_url": image_url}
    smhc_database.child("OpenCV-Danger").set(data_database)
    print ("Success Push to Database OpenCV-Danger")
    #"""

while True:
    date_string = dt.datetime.now().strftime("%Y-%m-%d")
    time_string = dt.datetime.now().strftime("%H:%M:%S")
    prove_image_normal = "Prove-Normal/image-{}-{}.png".format(date_string, time_string)
    prove_image_danger = "Prove-Danger/image-{}-{}.png".format(date_string, time_string)
    # Take frame-by-frame
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = faceCascade.detectMultiScale(gray, 1.1, 5)
    # Face box in camera
    for (x, y, w, h) in face:
        roi_gray = gray[y:y + h, x:x + w]
        roi_input = cv2.resize(roi_gray, (48, 48))
        
        pred = model.predict_emotion(roi_input[np.newaxis, :, :, np.newaxis])
        
        if pred == "Angry" or "Fear" or "Sad":
            danger_state += 1
        
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.putText(frame, pred, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)

    cv2.putText(frame, 'Face Detected : '+ str(len(face)), (30, 30), cv2.FONT_HERSHEY_SIMPLEX,  1, (0, 255, 0), 2)
    cv2.imshow('Video', frame)

    current_time = dt.datetime.now()
    delta = current_time-t
    # Capture Webcam
    if delta.seconds >= 5:
        # Capture danger
        if danger_state > 400:
            take_capture_2(frame)
            print ("Total danger current state: {}".format(danger_state))
            fcm.sendPush("Warning", "The rate of suicide increases, the person need help or counseling", FCM_tokens)
            danger_state = 0
            t = current_time.now()
        else:
            take_capture_1(frame)
            t = current_time.now()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
