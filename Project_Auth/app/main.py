import uvicorn
from fastapi import FastAPI
from .database import init_db
from .auth import router as auth_router
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

app = FastAPI()

app.add_event_handler("startup", init_db)

app.include_router(auth_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=8000)