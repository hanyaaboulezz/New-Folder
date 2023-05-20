from flask import Flask, jsonify, request
from flask_restful import Resource
import json
import firebase_admin
import pyrebase
from firebase_admin import credentials
from firebase_admin import db
from flask import Flask, jsonify, request
from flask_cors import CORS
from  flask_restful import Resource, Api
import json
import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase
import h5py
import pandas as pd
import librosa
import numpy as np
from flask_cors import CORS
import tensorflow as tf
from tensorflow import keras
from scipy.io import wavfile as wav
from tqdm import tqdm
import wave
from sklearn.preprocessing import LabelEncoder
import time
import threading

response= ""


app= Flask(__name__)
api= Api(app)

config = {
    "apiKey": "AIzaSyDXnn-Nizd97gjj9rH6RkK0mpy6pDGWnqs",
    "authDomain": "appdataset.firebaseapp.com",
    "databaseURL": "https://appdataset-default-rtdb.firebaseio.com",
    "projectId": "appdataset",
    "storageBucket": "appdataset.appspot.com",
    "messagingSenderId": "776258012612",
    "appId": "1:776258012612:web:6d85e6c31c0fc66dd49091",
    "measurementId": "G-HZRD5W3JVM"

  }

firebase_storage = pyrebase.initialize_app(config)
storage = firebase_storage.storage()

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()






def audio_prediction(filename):
    audio, sample_rate = librosa.load(filename, res_type='kaiser_fast')
    mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)
    mfccs_scaled_features = mfccs_scaled_features.reshape(1, -1)
    labelencoder = LabelEncoder()
    model = tf.keras.models.load_model('C:\\Users\\user\\RPW_model0.h5')
    x_predict = model.predict(mfccs_scaled_features)
    predicted_label = np.argmax(x_predict, axis=1)
    print(predicted_label)
    return str(predicted_label)

def doAll(treeid):
    path_on_cloud = treeid

    storage.child(path_on_cloud).download("C:\\Users\\user\\New folder\\", path_on_cloud)

    if (audio_prediction("C:\\Users\\user\\New folder\\"+path_on_cloud)== "[0]"):
        audio_class = "RPW"
        print(audio_class)
        db.collection('tree').document(treeid).update({"Infected": True})

    else:
        audio_class = "negative"
        print(audio_class)
        db.collection('tree').document(treeid).update({"Infected": False})    


@app.route('/farm', methods =['GET', 'POST'])
def nameRoute():
    global response

    if(request.method == 'POST'):
        request_data = request.data
        request_data = json.loads(request_data)
        name = request_data['farm']
        response = f'hi'
        for i in range(len(name)):
            print(name[i])
            doAll(name[i])

        return ""
    else:
        return jsonify({'farm': response})
    

if __name__ == "__main__":
    app.run(debug=True)
