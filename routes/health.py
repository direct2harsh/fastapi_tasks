from fastapi import APIRouter, Depends
from auth.auth_config import validate_admin_user
from db.connection import get_db
from sqlalchemy.orm import Session
from sqlalchemy import  text


from models.auth_models import AuthenticatedUser

router = APIRouter(prefix="/health",tags=["Health Check"])



@router.get("/")
def check_app_health():
    """Check if the app is running and reachable"""
    return "App is running fine" 

@router.get("/db/", )
def check_db_health(db:Session = Depends(get_db),user:AuthenticatedUser= Depends(validate_admin_user)):

    """Only Admin User can access this endpoint, 
        This is just for demo, where one admin role is being sent for admin client
    """
    query = "SELECT count(id) FROM tasks"
    try:
        db.execute(text(query))
        return "DB is connected."
    except Exception as e:
        return f"DB connection failed with error: {e}"
    
