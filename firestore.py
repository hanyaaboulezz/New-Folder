import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred)



db = firestore.client()
db.collection('tree').document('i1zWaNqtHXFUTOI4CAiH').update({"Infected": False})
