from fastapi import APIRouter, Depends
from db.connection import get_db
from sqlalchemy.orm import Session
from sqlalchemy import  text

router = APIRouter(prefix="/health")



@router.get("/")
def check_app_health():
    """Check if the app is running and reachable"""
    return "App is running fine" 

@router.get("/db/")
def check_db_health(db:Session = Depends(get_db)):
    query = "SELECT count(id) FROM tasks"
    try:
        db.execute(text(query))
        return "DB is connected."
    except Exception as e:
        return f"DB connection failed with error: {e}"
    
