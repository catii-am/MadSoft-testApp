from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from public_api import models
from public_api import schemas
from public_api import crud
from public_api.database import engine, SessionLocal
from fastapi_pagination import add_pagination, paginate, Page

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/memes', response_model=schemas.Meme)
def create_meme(meme: schemas.MemeCreate, db: Session = Depends(get_db)):
    return crud.create_meme(db, meme)


@app.get('/memes', response_model=Page[schemas.Meme])
def read_memes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    memes = crud.get_memes(db, skip, limit)
    return paginate(memes)


@app.get('/memes/{meme_id}', response_model=schemas.Meme)
def read_meme_by_id(meme_id: int, db: Session = Depends(get_db)):
    db_meme = crud.get_meme(db, meme_id)
    if db_meme is None:
        raise HTTPException(status_code=404, detail='Meme not found')
    return db_meme


@app.put('/memes/{meme_id}', response_model=schemas.Meme)
def update_meme_by_id(meme_id: int, meme: schemas.MemeCreate, db: Session = Depends(get_db)):
    return crud.update_meme(db, meme_id, meme)


@app.delete('/memes/{meme_id}')
def delete_meme_by_id(meme_id: int, db: Session = Depends(get_db)):
    return crud.delete_meme(db, meme_id)


if __name__ == '__main__':
    add_pagination(app)
