from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, field_validator 
from typing import Literal, Annotated
import pickle
import pandas as pd
from model.predict import predict_output,model
from schema.prediction_response import PredictionResponse
from schema.user_input import UserInput
#import model

app = FastAPI()



#now endpoint
#this is human readable endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the Insurance Premium Prediction API!"}
#machine readable like in cloude serrvice
@app.get("/health")
def health_check():
    return {"status": "ok",
            "model_loaded": True if model else False,} 
@app.post("/predict",response_model=PredictionResponse)
def predict_premium(data: UserInput):
    input_data = {
        "bmi": data.bmi,
        "lifestyle_risk": data.lifestyle_risk(),
        "age_group": data.age_group(),
        "city_tier": data.city_tier,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation,
    }
    try:
        prediction = predict_output(input_data)
        return JSONResponse(content={"response": prediction}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    