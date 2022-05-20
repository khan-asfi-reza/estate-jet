from functools import lru_cache

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from estatejet.config.settings import Settings
from estatejet.db import Base, engine
from estatejet.dependencies import DbSession, get_db
from estatejet.schemas.item import Item
from estatejet.models.item import Item as ItemModel

app = FastAPI()

Base.metadata.create_all(bind=engine)


@lru_cache()
def get_settings():
    return Settings()


@app.get("/")
async def root(settings: Settings = Depends(get_settings)):
    return {"message": "Welcome To EstateJet"}


@app.get("/item", response_model=list[Item])
async def item_get():
    items = [
        Item(name="Glass", description="Glass for home"),
        Item(name="Floor", description="Floor for home"),
        Item(name="Door", description="Door for home"),
    ]
    return items


@app.post("/item", response_model=Item)
async def item_post(item: Item, db: Session = Depends(get_db)):
    db_item = ItemModel(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
