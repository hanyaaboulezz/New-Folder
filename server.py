from fastapi import FastAPI
from  fastapi import UploadFile, File
import uvicorn


app = FastAPI()

@app.get('/index')
def hello_world(name :str):
    return f"Hello {name}!"

@app.post('api/predict')
async def predict_audio(file: UploadFile = File(...)):
    wavefile= prediction.read_audio(file)
    mfccs_scaled_features= prediction.preprocess(wavefile)
    prediction= prediction.mdodel_predict(mfccs_scaled_features)





if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')