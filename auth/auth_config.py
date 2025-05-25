from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
import jwt
from services.logging_service import logger

from models.auth_models import AuthenticatedUser

# For localHost
# KEYCLOAK_SERVER_URL = "http://localhost:8080/" 
# For Docker
KEYCLOAK_SERVER_URL = "http://keycloak:8080/"
KEYCLOAK_REALM = "tasks-realm"
NORMAL_CLIENT_ID = "tasks-client"
ADMIN_CLIENT_ID = "admin-client"
KEYCLOAK_ISSUER_URL = f"{KEYCLOAK_SERVER_URL}realms/{KEYCLOAK_REALM}"
KEYCLOAK_JWKS_URL = f"{KEYCLOAK_SERVER_URL}realms/{KEYCLOAK_REALM}/protocol/openid-connect/certs"
KEYCLOAK_TOKEN_URL = f"{KEYCLOAK_SERVER_URL}realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"




oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=KEYCLOAK_TOKEN_URL
   
)




async def validate_current_user(token: str = Depends(oauth2_scheme)) -> AuthenticatedUser:
    """
    Validates the JWT token and extracts user information.
    """
    try:
        # Get the signing key from JWKS
        jwks = jwt.PyJWKClient(KEYCLOAK_JWKS_URL,cache_keys=True)
        signing_key =jwks.get_signing_key_from_jwt(token)
        print(signing_key)

        # Decode and validate the token
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"], # Keycloak typically uses RS256
            audience=NORMAL_CLIENT_ID, # Your Keycloak client ID
            issuer=KEYCLOAK_ISSUER_URL,
            options={"verify_exp": True, "verify_aud": False, "verify_iss": True}
        )

        # Extract user data from payload
        user_id = payload.get("sub")
        username = payload.get("preferred_username")
        email = payload.get("email")

        # Keycloak roles are often in realm_access.roles or resource_access.<client_id>.roles
        roles = []
        if "realm_access" in payload and "roles" in payload["realm_access"]:
            roles.extend(payload["realm_access"]["roles"])
        if "resource_access" in payload and NORMAL_CLIENT_ID in payload["resource_access"] \
           and "roles" in payload["resource_access"][NORMAL_CLIENT_ID]:
            roles.extend(payload["resource_access"][NORMAL_CLIENT_ID]["roles"])

        if not user_id or not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: Missing required user information",
                headers={"WWW-Authenticate": "Bearer"}, 
            )

        return AuthenticatedUser(
            id=user_id,
            username=username,
            email=email,
            roles=list(set(roles)) 
        )

    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
   
    except jwt.exceptions.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.exceptions.InvalidIssuerError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except Exception as e:
        # Catch any other unexpected errors during token processing
        print(f"Unexpected error during token validation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during authentication.",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def validate_admin_user(token: str = Depends(oauth2_scheme)) -> AuthenticatedUser:
    """
    Validates the JWT token and extracts user information.
    """
    try:
        logger.critical("Admin action invoked")
        # Get the signing key from JWKS
        jwks = jwt.PyJWKClient(KEYCLOAK_JWKS_URL,cache_keys=True)
        signing_key =jwks.get_signing_key_from_jwt(token)
        print(signing_key)

        # Decode and validate the token
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"], # Keycloak typically uses RS256
            audience=ADMIN_CLIENT_ID, # Your Keycloak client ID
            issuer=KEYCLOAK_ISSUER_URL,
            options={"verify_exp": True, "verify_aud": False, "verify_iss": True}
        )

        # Extracting user Details
        user_id = payload.get("sub")
        username = payload.get("preferred_username")
        email = payload.get("email")

        # Keycloak roles + The Admin Role Validation
        roles = []
        if "realm_access" in payload and "roles" in payload["realm_access"]:
            roles.extend(payload["realm_access"]["roles"])
        if "resource_access" in payload and ADMIN_CLIENT_ID in payload["resource_access"] \
           and "roles" in payload["resource_access"][ADMIN_CLIENT_ID]:
            roles.extend(payload["resource_access"][ADMIN_CLIENT_ID]["roles"])
        else:
            raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not authorized for this action",)   

        if not user_id or not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: Missing required user information",
                headers={"WWW-Authenticate": "Bearer"}, 
            )

        return AuthenticatedUser(
            id=user_id,
            username=username,
            email=email,
            roles=list(set(roles)) 
        )
    # Below exception will throw when HTTP exception is being raise based on Admin auth
    except HTTPException:
        raise

    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
   
    except jwt.exceptions.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.exceptions.InvalidIssuerError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except Exception as e:
        # Catch any other unexpected errors during token processing
        print(f"Unexpected error during token validation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during authentication.",
            headers={"WWW-Authenticate": "Bearer"},
        )
