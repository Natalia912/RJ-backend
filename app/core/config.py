from dotenv import load_dotenv
from os import getenv


load_dotenv() 

DATABASE_CONFIG = {
    "HOST": getenv("PG_HOST"),
    "PORT": getenv("PG_PORT"),
    "USER": getenv("PG_USER"),
    "PASSWORD": getenv("PG_PASSWORD"),
    "NAME": getenv("PG_DATABASE")
}

JWT_CONFIG = {
    "SECRET_KEY": getenv("SECRET_KEY"),
    "ALGORITHM": getenv("ALGORITHM"),
    "ACCESS_TOKEN_EXPIRE_MINUTES": int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
}