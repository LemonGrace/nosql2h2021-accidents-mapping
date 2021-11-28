from pathlib import Path, PurePosixPath

import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config

# MONGO_DETAILS = config('MONGO_DETAILS') # read environment variable.
MONGO_DETAILS = "mongodb://localhost:27017"
# MONGO_DETAILS = MONGO_DETAILS

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.cars

car_collection = database.get_collection("car_collection")


# Функция для преобразования данных из бд в словарь
def car_helper(car) -> dict:
    return {
        "id": str(car["_id"]),
        "brand": car["brand"],
        "models": car['models']
    }


# Получить все автомобили, присутствующие в базе данных
async def retrieve_cars():
    cars = []
    async for car in car_collection.find():
        cars.append(car_helper(car))
    return cars


# Добавить новый автомобиль в базу данных
async def add_car(car_data: dict) -> dict:
    car = await car_collection.insert_one(car_data)
    new_car = await car_collection.find_one({"_id": car.inserted_id})
    return car_helper(new_car)


# Получить все автомобили, присутствующие в базе данных
async def retrieve_cars_brands():
    cars = []
    async for car in car_collection.find():
        data = {'brand': car["brand"], 'logo': PurePosixPath("source", "image", "brands", str(car["brand"]).upper() + ".jpg")}
        cars.append(data)
    return list(cars)

# Получить автомобили соответствующей марки
async def retrieve_car_on_brand(brand: str) -> list:
    car = await car_collection.find_one({"brand": brand})
    if car:
        arr = []
        for item in car['models']:
            model = {'modelName': item['modelName'],
                     'firstYearProduction': item['firstYearProduction'],
                     'generations_count': len(item['generations']),
                     }
            if 'engineType' in item:
                model['engineType'] = item['engineType']
            if 'style' in item:
                model['style'] = item['style']
            if 'generations' in item:
                model['generations_count'] = len(item['generations'])
            else:
                model['generations_count'] = 0
            arr.append(model)
        return arr


# Получить автомобили соответствующей марки
async def retrieve_generations_car(brand: str, model_name: str) -> list:
    data = await car_collection.find_one({'brand': brand, 'models': {'$elemMatch': {'modelName': model_name}}},
                                         {'models.$': 1})
    model_name = model_name.replace(' ', '_')
    if data:
        model_data = data['models'][0]
        if'generations' in model_data:
            for i, gen in enumerate(model_data['generations']):
                model_data['generations'][i]['image'] = PurePosixPath("source", "image", "generations",
                                                                      brand.upper(), model_name,
                                                                      str(gen['fullName']).replace(' ', '_') + '.jpg')
            return model_data['generations']

# Получить автомобиль с соответствующим ID
async def retrieve_car(id: str) -> dict:
    car = await car_collection.find_one({"_id": ObjectId(id)})
    if car:
        return car_helper(car)


# Обновите автомобиль с помощью соответствующего ID
async def update_car(id: str, data: dict):
    # Возвращает значение false, если отправляется пустое тело запроса.
    if len(data) < 1:
        return False
    car = await car_collection.find_one({"_id": ObjectId(id)})
    if car:
        updated_car = await car_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_car:
            return True
        return False


# Удалить автомобиль из базы данных по ID
async def delete_car(id: str):
    car = await car_collection.find_one({"_id": ObjectId(id)})
    if car:
        await car_collection.delete_one({"_id": ObjectId(id)})
        return True