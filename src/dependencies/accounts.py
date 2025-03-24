from dotenv import load_dotenv
import os
from security.interfaces import JWTAuthManagerInterface
from security.jwt_auth_manager import JWTAuthManager

load_dotenv()

def get_jwt_auth_manager() -> JWTAuthManagerInterface:
    secret_key_access = os.getenv("SECRET_KEY_ACCESS")
    secret_key_refresh = os.getenv("SECRET_KEY_REFRESH")
    algorithm = os.getenv("JWT_SIGNING_ALGORITHM", "HS256")

    if not secret_key_access or not isinstance(secret_key_access, (str, bytes)):
        raise ValueError("SECRET_KEY_ACCESS must be a string or bytes.")
    if not secret_key_refresh or not isinstance(secret_key_refresh, (str, bytes)):
        raise ValueError("SECRET_KEY_REFRESH must be a string or bytes.")

    return JWTAuthManager(
        secret_key_access=secret_key_access,
        secret_key_refresh=secret_key_refresh,
        algorithm=algorithm
    )
