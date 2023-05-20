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



response =''

app = Flask(__name__)

CORS(app)

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

boolValue=False

callback_done = threading.Event()




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

    storage.child(path_on_cloud).download("C:\\Users\\user\\New folder\\test", path_on_cloud)

    if (audio_prediction("C:\\Users\\user\\New folder\\"+path_on_cloud)== "[0]"):
        audio_class = "RPW"
        print(audio_class)
        db.collection('tree').document(treeid).update({"Infected": True})

    else:
        audio_class = "negative"
        print(audio_class)
        db.collection('tree').document(treeid).update({"Infected": False})    

# Create an Event for notifying main thread.
# delete_done = threading.Event()

# Create a callback on_snapshot function to capture changes





@app.route('/name', methods =['GET', 'POST'])
def nameRoute():
    global response

    if (request.method == 'POST'):
        request_data= request.data
        request_data = json.loads(request_data.decode('utf-8'))
        id = request_data['name']
        
        response = f'processing sound'
        return " "
    else:
        return jsonify({'name' : response})





if __name__ == '__main__':
    app.run(debug=True)



def on_snapshot(col_snapshot, changes, read_time):
    print('NEW AUDIOS')
    for change in changes:
        if change.type.name == 'ADDED':
            result=db.collection('storageRef').document(change.document.id).get()
            print(result.to_dict())
        #elif change.type.name == 'MODIFIED':
         #   print(f'Modified data')
        #elif change.type.name == 'REMOVED':
         #   print(f'Removed data')
            #delete_done.set()
    #callback_done.set()


col_query = db.collection('storageRef')

# Watch the collection query
query_watch = col_query.on_snapshot(on_snapshot)



while True:
    print('processing...')
    time.sleep(1 )
    