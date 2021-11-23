import datetime
from typing import Optional, Set, List

from pydantic import BaseModel, Field


class RTASchema(BaseModel):
    year: int = Field(...)
    brand: str = Field(...)
    model: str = Field(...)
    size: str = Field(...)
    modelType: str = Field(...)
    overallDeathRate: int = Field(...)
    multivehicleCrashDeathRate: int = Field(...)
    singlevehicleCrashDeathRate: int = Field(...)

    class Config:
        schema_extra = {
            "example":
                {
                    "year": "2017",
                    "brand": "Kia",
                    "model": "Rio",
                    "size": "mini",
                    "modelType": "four-door cars",
                    "overallDeathRate": "87 (40-134)",
                    "multivehicleCrashDeathRate": "51",
                    "singlevehicleCrashDeathRate": "38"
                }
        }


class UpdateRTAModel(BaseModel):
    brand: Optional[str]
    year:  Optional[int]
    brand: Optional[str]
    model: Optional[str]
    size: Optional[str]
    modelType: Optional[str]
    overallDeathRate: Optional[int]
    multivehicleCrashDeathRate: Optional[int]
    singlevehicleCrashDeathRate: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                    "year": "2017",
                    "brand": "Kia",
                    "model": "Rio",
                    "size": "mini",
                    "modelType": "four-door cars",
                    "overallDeathRate": "87 (40-134)",
                    "multivehicleCrashDeathRate": "51",
                    "singlevehicleCrashDeathRate": "38"
                }
        }
