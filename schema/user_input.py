
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, field_validator 
from typing import Literal, Annotated
import pickle
import pandas as pd
from config.city_tier import tier_1_cities, tier_2_cities
#import model
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)
app = FastAPI()

#pydantic model for input data validation
class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=100, description="Age of the user", examples=[28])]
    weight: Annotated[float, Field(..., gt=0, lt=500, description="Weight of the user in kilograms", examples=[90.0])]
    height: Annotated[float, Field(..., gt=0, lt=4, description="Height of the user in meters", examples=[1.65])]
    income_lpa: Annotated[float, Field(..., gt=0, description="Income of the user in LPA", examples=[5.0])]
    smoker: Annotated[bool, Field(..., description="Whether the user is a smoker or not", examples=[True])]
    city: Annotated[str, Field(..., description="City of the user", examples=["chattogram"])]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'business_owner', 'government_job', 'private_job', 'unemployed'], Field(..., description="Occupation of the user", examples=["government_job"])]
    
    @field_validator('city')
    @classmethod
    def normalize_city(cls, value: str) -> str:
        return value.strip().title()
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2),  2)

    def lifestyle_risk(self) -> str:
        bmi_value = self.bmi
        if bmi_value < 18.5 and not self.smoker:
            return "low"
        elif bmi_value > 30 and self.smoker:
            return "high"
        elif 18.5 <= bmi_value < 25 or self.smoker:
            return "medium"
        return "low"

    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif 25 <= self.age < 45:
            return "adult"
        elif 45 <= self.age < 60:
            return "middle_aged"
        else:
            return "senior"

    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
    

