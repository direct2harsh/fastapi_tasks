from fastapi import FastAPI
import uvicorn
from db.connection import DeclarativeBase,engine
from routes import tasks,health
from db.connection import get_db



app = FastAPI()
PORT:int = 3216


# 
# DeclarativeBase.metadata.drop_all(engine)
DeclarativeBase.metadata.create_all(engine)

app.include_router(router=tasks.router)
app.include_router(router=health.router)





if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0",port=PORT, reload=True,workers=10)