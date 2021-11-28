from typing import Optional, List

from pydantic import BaseModel, Field


class MyBaseModel(BaseModel):
    def __hash__(self):  # make hashable BaseModel subclass
        return hash((type(self),) + tuple(self.__dict__.values()))


class GenerationSchema(MyBaseModel):
    fullName: str = Field(...)
    firstYearProduction: str = Field(...)
    lastYearProduction: str = Field(...)
    topSpeed: Optional[str]
    acceleration: Optional[str]
    lenght: Optional[str]
    width: Optional[str]
    height: Optional[str]
    wheelBase: Optional[str]
    wheelTrack: Optional[str]
    cargoVolume: Optional[str]
    aerodynamics: Optional[str]
    driveType: Optional[str]
    gearBox: Optional[str]
    fuel: Optional[str]


class ModelSchema(MyBaseModel):
    modelName: str = Field(...)
    firstYearProduction: str = Field(...)
    engineType: Optional[str] = Field(...)
    style: Optional[str] = Field(...)
    generations: Optional[List[GenerationSchema]]


class CarSchema(BaseModel):
    brand: str = Field(...)
    models: Optional[List[ModelSchema]]

    class Config:
        schema_extra = {
            "example": {
                "brand": "AUDI",
                "models": [
                    {
                        "modelName": "AUDI S8",
                        "firstYearProduction": "1996",
                        "engineType": "Gasoline",
                        "style": "",
                        "generations": [
                            {
                                "fullName": "AUDI S8",
                                "firstYearProduction": "2019",
                                "lastYearProduction": "2021",
                                "topSpeed": "249",
                                "acceleration": "3.8",
                                "lenght": "5179",
                                "width": "1946",
                                "height": "1473",
                                "wheelBase": "2997",
                                "wheelTrack": "1.628",
                                "cargoVolume": "504",
                                "aerodynamics": "0.27",
                                "driveType": "All Wheel Drive",
                                "gearBox": "8-speed automatic Tiptronic",
                                "fuel": "Gasoline"
                            }
                        ]
                    }
                ]
            }
        }


class UpdateModelModel(MyBaseModel):
    modelName: Optional[str]
    firstYearProduction: Optional[int]
    engineType: Optional[str]
    style: Optional[str]
    generations: Optional[List[GenerationSchema]]


class UpdateCarModel(BaseModel):
    brand: Optional[str]
    models: List[ModelSchema]

    class Config:
        schema_extra = {
            "example": {
                "brand": "AUDI",
                "models": [
                    {
                        "modelName": "AUDI S8",
                        "firstYearProduction": "1996",
                        "engineType": "Gasoline",
                        "style": "",
                        "generations": [
                            {
                                "fullName": "AUDI S8",
                                "firstYearProduction": "2019",
                                "lastYearProduction": "2021",
                                "topSpeed": "249",
                                "acceleration": "3.8",
                                "lenght": "5179",
                                "width": "1946",
                                "height": "1473",
                                "wheelBase": "2997",
                                "wheelTrack": "1.628",
                                "cargoVolume": "504",
                                "aerodynamics": "0.27",
                                "driveType": "All Wheel Drive",
                                "gearBox": "8-speed automatic Tiptronic",
                                "fuel": "Gasoline"
                            }
                        ]
                    }
                ]
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}