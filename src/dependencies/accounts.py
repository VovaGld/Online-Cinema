from dotenv import load_dotenv
import os

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from repositories.accounts_rep import UserRepository
from security.http import get_token
from security.interfaces import JWTAuthManagerInterface
from security.jwt_auth_manager import JWTAuthManager
from storages import S3StorageInterface, S3StorageClient

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


def get_user_repository(
        session: AsyncSession = Depends(get_db),
        JWTmanager: JWTAuthManager = Depends(get_jwt_auth_manager),
        token: str = Depends(get_token)
) -> UserRepository:
    return UserRepository(session=session, JWTmanager=JWTmanager, token=token)


def get_s3_storage_client() -> S3StorageInterface:
    endpoint_url = os.getenv('S3_ENDPOINT', 'http://localhost:9000')
    access_key = os.getenv('MINIO_ROOT_USER', 'minioadmin')
    secret_key = os.getenv('MINIO_ROOT_PASSWORD', 'minioadmin')
    bucket_name = os.getenv('MINIO_STORAGE', 'online-cinema-bucket')

    return S3StorageClient(
        endpoint_url=endpoint_url,
        access_key=access_key,
        secret_key=secret_key,
        bucket_name=bucket_name
    )