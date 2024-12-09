import uvicorn
from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routes import router

app = FastAPI()

create_db_and_tables()

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)