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


# input_shape =[1, 40]


def read_audio(wav_audio):
    wavefile = wave.open(wav_audio, 'rb')
    return wavefile


def preprocess(wavefile):
    sample_rate=22050
    audio = wavefile
    mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)
    mfccs_scaled_features = mfccs_scaled_features.reshape(1, -1)
    return mfccs_scaled_features

def mdodel_predict(mfccs_scaled_features):
    labelencoder = LabelEncoder()
    model = tf.keras.models.load_model('RPW_model0.h5')
    x_predict = model.predict(mfccs_scaled_features)
    predicted_label = np.argmax(x_predict, axis=1)
    print(predicted_label)
    prediction = labelencoder.inverse_transform(predicted_label)


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


if (audio_prediction("C:\\Users\\user\\New folder\\3minfeeding-13.wav")== "[0]"):
    audio_class = "RPW"
    print(audio_class)