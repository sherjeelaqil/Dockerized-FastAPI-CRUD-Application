from fastapi import FastAPI
from app.common import database, init_db
from app.models import users_models
from app.routes.users_routes import router as api_router
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
users_models.Base.metadata.create_all(bind=database.engine)

app.include_router(api_router)

@app.on_event("startup")
def on_startup():
    init_db.initialize_database()