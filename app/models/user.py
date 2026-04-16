from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True)
    hashed_password: str

class UserPublic(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True)



