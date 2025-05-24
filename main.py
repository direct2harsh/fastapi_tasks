from fastapi import FastAPI
import uvicorn
from db.connection import DeclarativeBase,engine
from routes import tasks,health,auth
from fastapi.middleware.cors import CORSMiddleware





app = FastAPI(title="Task Management System")
PORT:int = 3216


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
   
)

 

try:
    # DeclarativeBase.metadata.drop_all(engine)
    DeclarativeBase.metadata.create_all(engine)
except Exception as e:
    print("Error creating database metadata")
    print(e)    

app.include_router(router=tasks.router)
app.include_router(router=health.router)
app.include_router(router=auth.router)





if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0",port=PORT, reload=True,workers=10)