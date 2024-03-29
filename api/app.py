from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import date
import os
import pickle
import pandas as pd
import numpy as np
import math
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import uvicorn
from enum import Enum
from pathlib import Path


# Set port to the env variable PORT to make it easy to choose the port on the server
# If the Port env variable is not set, use port 8000
PORT = os.environ.get("PORT", 8000)
app = FastAPI(port=PORT)

#_____loading the models____
__version__ = "0.1.0"

# #____setting BASE_DIR for easy use with Docker____
# BASE_DIR = Path(__file__).resolve(strict=True).parent

# with open(f"{BASE_DIR}/api/models/rfr_app_model_with_pipeline-{__version__}.pkl", "rb") as file:
#     apartement_model = pickle.load(file)

# with open(f"{BASE_DIR}/api/models/rfr_house_model_with_pipeline-{__version__}.pkl", "rb") as file:
#     house_model = pickle.load(file)

with open(f"rfr_app_model_with_pipeline-{__version__}.pkl", "rb") as file:
    apartment_model = pickle.load(file)

with open(f"rfr_house_model_with_pipeline-{__version__}.pkl", "rb") as file:
    house_model = pickle.load(file)


class ApartmentPropertySubtypeEnum(str, Enum):
    APARTMENT = "APARTMENT"
    DUPLEX = "DUPLEX"
    FLAT_STUDIO = "FLAT_STUDIO"
    GROUND_FLOOR = "GROUND_FLOOR"
    KOT = "KOT"
    LOFT = "LOFT"
    PENTHOUSE = "PENTHOUSE"
    SERVICE_FLAT = "SERVICE_FLAT"
    TRIPLEX = "TRIPLEX"

class ApartmentKitchenTypeEnum(str, Enum):
    HYPER_EQUIPPED = "HYPER_EQUIPPED"
    INSTALLED = "INSTALLED"
    NOT_INSTALLED = "NOT_INSTALLED"
    SEMI_EQUIPPED = "SEMI-EQUIPPED"
    USA_INSTALLED = "USA_INSTALLED"
    USA_SEMI_EQUIPPED = "USA_SEMI_EQUIPPED"
    USA_UNINSTALLED = "USA_UNINSTALLED"
    nan = None

class HousePropertySubtypeEnum(str, Enum):
    HOUSE = "HOUSE"
    MIXED_USE_BUILDING = "MIXED_USE_BUILDING"
    APARTMENT_BLOCK = "APARTMENT_BLOCK"
    BUNGALOW = "BUNGALOW"
    VILLA = "VILLA"
    EXCEPTIONAL_PROPERTY = "EXCEPTIONAL_PROPERTY"
    COUNTRY_COTTAGE = "COUNTRY_COTTAGE"
    MANSION = "MANSION"
    FARMHOUSE = "FARMHOUSE"
    TOWN_HOUSE = "TOWN_HOUSE"
    MANOR_HOUSE = "MANOR_HOUSE"
    CHALET = "CHALET"
    OTHER_PROPERTY = "OTHER_PROPERTY"

class HouseKitchenTypeEnum(str, Enum):
    INSTALLED = "INSTALLED"
    USA_HYPER_EQUIPPED = "USA_HYPER_EQUIPPED"
    NOT_INSTALLED = "NOT_INSTALLED"
    HYPER_EQUIPPED = "HYPER_EQUIPPED"
    SEMI_EQUIPPED = "SEMI_EQUIPPED"
    USA_SEMI_EQUIPPED = "USA_SEMI_EQUIPPED"
    NAN = None
    USA_INSTALLED = "USA_INSTALLED"
    USA_UNINSTALLED = "USA_UNINSTALLED"

class StateOfBuildingEnum(str, Enum):
    AS_NEW = "AS_NEW"
    GOOD = "GOOD"
    JUST_RENOVATED = "JUST_RENOVATED"
    TO_BE_DONE_UP = "TO_BE_DONE_UP"
    TO_RENOVATE = "TO_RENOVATE"
    TO_RESTORE = "TO_RESTORE"
    nan = None

class ProvinceEnum(str, Enum):
    ANTWERPEN = "antwerpen"
    BRUSSEL = "brussel"
    HENEGOUWEN = "henegouwen"
    LIMBURG = "limburg"
    LUIK = "luik"
    LUXEMBURG = "luxemburg"
    NAMEN = "namen"
    OOST_VLAANDEREN = "oost-vlaanderen"
    VLAAMS_BRABANT = "vlaams-brabant"
    WAALS_BRABANT = "waals-brabant"
    WEST_VLAANDEREN = "west-vlaanderen"


class ApartmentPropertyData(BaseModel):
    postal_code: Optional[int] = Field(9000, description="The postal code of the property", ge=1000, lt=10000)
    property_subtype: Optional[ApartmentPropertySubtypeEnum] = ApartmentPropertySubtypeEnum.APARTMENT
    number_of_rooms: Optional[float] = 3
    living_area: Optional[float]=25
    kitchen_type: Optional[ApartmentKitchenTypeEnum] = ApartmentKitchenTypeEnum.HYPER_EQUIPPED
    furnished: Optional[int] = Field(1, description="Is the property furnished or not", ge=0, lt=2)
    open_fire: Optional[int] = Field(1, description="Does the property have an open fire or not", ge=0, lt=2)
    terrace: Optional[float] = Field(1, description="Does the property have a terrace or not", ge=0, lt=2)
    terrace_area: Optional[float]=10
    garden: Optional[float] = Field(1, description="Does the property have a garden or not", ge=0, lt=2)
    garden_area: Optional[float]=10
    number_of_facades: Optional[float]=2
    swimming_pool: Optional[float] = Field(1, description="Does the property have a swimming pool or not", ge=0, lt=2)
    state_of_building: Optional[StateOfBuildingEnum] = StateOfBuildingEnum.GOOD
    province: Optional[ProvinceEnum] = ProvinceEnum.ANTWERPEN

class HousePropertyData(BaseModel):
    postal_code: Optional[int] = Field(9000, description="The postal code of the property", ge=1000, lt=10000)
    property_subtype: Optional[HousePropertySubtypeEnum] = HousePropertySubtypeEnum.HOUSE
    number_of_rooms: Optional[float] = 4
    living_area: Optional[float]=200
    kitchen_type: Optional[HouseKitchenTypeEnum] = HouseKitchenTypeEnum.HYPER_EQUIPPED
    furnished: Optional[int] = Field(1, description="Is the property furnished or not", ge=0, lt=2)
    open_fire: Optional[int] = Field(1, description="Does the property have an open fire or not", ge=0, lt=2)
    terrace: Optional[float] = Field(1, description="Does the property have a terrace or not", ge=0, lt=2)
    terrace_area: Optional[float]=50
    garden: Optional[float] = Field(1, description="Does the property have a garden or not", ge=0, lt=2)
    garden_area: Optional[float]=30
    surface_of_good: Optional[float]=300
    number_of_facades: Optional[float]=4
    swimming_pool: Optional[float] = Field(1, description="Does the property have a swimming pool or not", ge=0, lt=2)
    state_of_building: Optional[StateOfBuildingEnum] = StateOfBuildingEnum.GOOD
    province: Optional[ProvinceEnum] = ProvinceEnum.ANTWERPEN

@app.get("/")
async def root():
    """ Route that returns health check and model version if the server runs """
    return {"health_check": "ok", "model_version": __version__}

@app.post("/predict/apartment")
async def predict(app_data: ApartmentPropertyData):
    try:
        # convert input data to dataframe for prediction
        X_test = pd.DataFrame([app_data.dict()])
        app_predictions = apartment_model.predict(X_test)
        return {app_predictions[0]}
    except ValueError:
        return {"error": "Invalid input. Please provide valid data."}

@app.post("/predict/house")
async def predict(app_data: HousePropertyData):
    try:
        # convert input data to dataframe for prediction
        X_test = pd.DataFrame([app_data.dict()])
        house_predictions = house_model.predict(X_test)
        return {house_predictions[0]}
    except ValueError:
        return {"error": "Invalid input. Please provide valid data."}


# underneath for debugging purposes
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
