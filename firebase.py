import pyrebase

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

path_on_cloud = "Jetson/192.168.1.5 (12)"

storage.child(path_on_cloud).download("192.168.1.5 (12).wav")