from sqlmodel import SQLModel

class LoginRequest(SQLModel):
    username: str | None = None
    email: str | None = None
    password: str