from pydantic import BaseModel, EmailStr


class BaseEmailPasswordSchema(BaseModel):
    email: EmailStr
    password: str

    model_config = {"from_attributes": True}


class UserRegistrationRequestSchema(BaseEmailPasswordSchema):
    pass


class UserLoginRequestSchema(BaseEmailPasswordSchema):
    pass


class UserLoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserRegistrationResponseSchema(BaseModel):
    id: int
    email: EmailStr

    model_config = {"from_attributes": True}


class UserActivationRequestSchema(BaseModel):
    email: EmailStr
    token: str


class MessageResponseSchema(BaseModel):
    message: str


class TokenRefreshRequestSchema(BaseModel):
    refresh_token: str


class TokenRefreshResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PasswordResetRequestSchema(BaseModel):
    email: EmailStr


class PasswordResetCompleteRequestSchema(BaseEmailPasswordSchema):
    token: str
