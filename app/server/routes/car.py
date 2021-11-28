from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
    add_car,
    delete_car,
    retrieve_car,
    retrieve_cars,
    update_car,
    retrieve_cars_brands,
    retrieve_car_on_brand, retrieve_generations_car
)
from app.server.models.car import (
    ErrorResponseModel,
    ResponseModel,
    CarSchema,
    UpdateCarModel,
)

router = APIRouter()

# Список марок машин
@router.get("/brands", response_description="Возвращает список марок.")
async def get_cars_brands():
    cars = await retrieve_cars_brands()
    if cars:
        return ResponseModel(cars, "Cars data retrieved successfully")
    return ResponseModel(cars, "Empty list returned")


# Информация о машинах определенной марки
@router.get("/{brand}", response_description="Возвращает список моделей машин определенной марки.")
async def get_cars_on_brand(brand: str):
    car = await retrieve_car_on_brand(brand)
    if car:
        return ResponseModel(car, "Car data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Car doesn't exist.")


# Информация о поколениях модели
@router.get("/{brand}/{model}", response_description="Возвращает список поколений машин определенной модели и марки.")
async def get_generations_car(brand: str, model: str):
    car = await retrieve_generations_car(brand, model)
    if car:
        return ResponseModel(car, "Car data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Car doesn't exist.")

# Информация о всех машинах
@router.get("/", response_description="Cars retrieved")
async def get_cars():
    cars = await retrieve_cars()
    if cars:
        return ResponseModel(cars, "Cars data retrieved successfully")
    return ResponseModel(cars, "Empty list returned")

# Информация о машине по индексу
@router.get("/{id}", response_description="Car data retrieved")
async def get_car_data(id):
    car = await retrieve_car(id)
    if car:
        return ResponseModel(car, "Car data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Car doesn't exist.")

# Добавление новой машины
@router.post("/", response_description="Car data added into the database")
async def add_car_data(car: CarSchema = Body(...)):
    car = jsonable_encoder(car)
    new_car = await add_car(car)
    return ResponseModel(new_car, "Car added successfully.")

#Обновление инфы о машине
@router.put("/{id}")
async def update_car_data(id: str, req: UpdateCarModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_car = await update_car(id, req)
    if updated_car:
        return ResponseModel(
            "Car with ID: {} name update is successful".format(id),
            "Car name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the Car data.",
    )


@router.delete("/{id}", response_description="Car data deleted from the database")
async def delete_car_data(id: str):
    deleted_car = await delete_car(id)
    if deleted_car:
        return ResponseModel(
            "Car with ID: {} removed".format(id), "Car deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Car with id {0} doesn't exist".format(id)
    )