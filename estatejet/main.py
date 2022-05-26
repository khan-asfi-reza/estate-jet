from fastapi import FastAPI

from estatejet.db import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

App = app


@app.get("/")
async def root():
    return {"message": "Welcome To EstateJet"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
