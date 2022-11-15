from fastapi import FastAPI
from database.db import engine
import uvicorn
from models import userModels
from routes.userRoutes import user_router

app = FastAPI()
app.debug  = True

userModels.Base.metadata.create_all(engine)

app.include_router(user_router, prefix="/users")

@app.get('/')
def index():
    return {"Pesan" : "Selamat Datang!"}

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)