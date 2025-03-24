from pydantic import BaseModel, EmailStr



class BaseEmailPasswordSchema(BaseModel):
    email: EmailStr
    password: str

    model_config = {
        "from_attributes": True
    }


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

    model_config = {
        "from_attributes": True
    }
