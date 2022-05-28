from fastapi import FastAPI

from estatejet.apps.user.models import User
from estatejet.apps.user.schema import UserCreateModel
from estatejet.db import Base, startup, Database

app = FastAPI()

App = app


@app.on_event("startup")
async def on_startup():
    await startup()


@app.get("/")
async def root():
    return {"message": "Welcome To EstateJet"}


@app.get("/create")
def create():
    user = UserCreateModel(email="email@gmai2l.com",
                           first_name="First Name",
                           last_name="Last Name",
                           country_code="+123",
                           phone_number="123456567",
                           role=1,
                           password="Password")

    data = User.create(user)
    return {"message": "Success"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
