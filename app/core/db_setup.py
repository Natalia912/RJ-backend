from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
from app.core.config import DATABASE_CONFIG

db_name = f"{DATABASE_CONFIG['USER']}:{DATABASE_CONFIG['PASSWORD']}@{DATABASE_CONFIG['HOST']}:{DATABASE_CONFIG['PORT']}/{DATABASE_CONFIG['NAME']}"
db_url = f"postgresql://{db_name}"

engine = create_engine(db_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]