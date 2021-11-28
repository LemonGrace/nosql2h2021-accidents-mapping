from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.server.routes.car import router as CarRouter

app = FastAPI()

origins = [
    "http://domainname.com",
    "https://domainname.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(CarRouter, tags=["Car"], prefix="/car")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to app!"}