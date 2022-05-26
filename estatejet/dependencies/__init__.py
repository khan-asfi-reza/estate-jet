from fastapi import Depends

from estatejet.db import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DatabaseSession = Depends(get_db)
