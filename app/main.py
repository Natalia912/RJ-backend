from fastapi import FastAPI
from app.core.db_setup import create_db_and_tables
from app.routers.user import router as user_router
from app.routers.auth import router as auth_router

async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
 

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(auth_router)

# @app.post("/test/")
# def create_test(test: Test, session: SessionDep):
#     session.add(test)
#     session.commit()
#     session.refresh(test)
#     return test

# @app.get("/test/")
# def read_tests(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(gt=0, le=100)] = 10):
#     tests = session.exec(select(Test).offset(offset).limit(limit)).all()
#     return tests
    
