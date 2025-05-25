# Creating this route to handle the creation on JWT token from docker.
# If using postman with localhost the jwt issuer will cause validation error.

from fastapi import APIRouter,HTTPException
from auth.auth_config import KEYCLOAK_TOKEN_URL
import requests
from models.auth_models import LoginModel
import json
from services.logging_service import logger

router = APIRouter(prefix= "/auth",tags=["Authorizations"])


@router.post("/getToken",)
async def getToken(creds:LoginModel):    

    payload = {"grant_type":"password",
               "client_id":creds.client_id, 
               "scope":"email openid" ,
               "username":creds.username,
               "password":creds.password}

    # payload = 'grant_type=password&client_id=admin-client&scope=email%20openid&username=harshvardhan%40admin.com&password=harsh'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", KEYCLOAK_TOKEN_URL, headers=headers, data=payload)

    resData = json.loads(response.content)
    
    if "access_token" not in resData:
  
        logger.critical("Check credentials " + "Username -" + creds.username)
        raise HTTPException(status_code= 401,detail="Check credentials")
        
    
    return resData
