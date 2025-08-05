from pydantic import EmailStr, SecretStr, Field, field_validator, ConfigDict, BaseModel, PositiveInt
from typing import Literal, Optional

class User(BaseModel):
    id: Optional[PositiveInt] = None
    name: str = Field(min_length=3, max_length=50)
    email: EmailStr = Field(max_length=100)
    rol: Optional[Literal["Librarian", "Client"]] = "Client"
    model_config = ConfigDict(
        validate_assignment=True,
        extra='ignore' 
    )

class UserAuth(User):
    model_config = ConfigDict(
        validate_default=True,
        validate_assignment=True,
        from_attributes=True
    )

    password: SecretStr = Field(min_length=8, max_length=255)

    @field_validator("password")
    def validar_password(cls, password_secret: SecretStr) -> SecretStr:
        p = password_secret.get_secret_value()

        havenumber = any(c.isdigit() for c in p)
        haveminus = any(c.islower() for c in p)
        havemayus = any(c.isupper() for c in p)

        if not (havenumber and haveminus and havemayus):
            raise ValueError(
                "La contraseña debe contener al menos: "
                "un número, una letra minúscula y una letra mayúscula."
            )

        return password_secret

class UserLogin(BaseModel):
    email: EmailStr
    password: SecretStr = Field(min_length=8, max_length=255)