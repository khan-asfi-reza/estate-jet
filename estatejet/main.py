from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from apps.auth.controllers import router as auth_router
from apps.users.controllers import router as user_router
from config import DATABASE_URL
from db import get_tortoise_models

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome To EstateJet"}


app.include_router(auth_router)
app.include_router(user_router)

register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": get_tortoise_models()},
    generate_schemas=True,
    add_exception_handlers=True,
)


