from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from models import Base
from database import engine
from routes import router
import uvicorn


Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["http://localhost:3000", "localhost:3000"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
