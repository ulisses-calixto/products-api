from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from . import actions, models, schemas
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI(title="Products-API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def healthcheck(db: Session = Depends(get_db)):
    checks = {
        "api": "ok",
        "postgres": "ok",
    }

    try:
        db.execute(text("SELECT 1"))
    except Exception:
        checks["postgres"] = "error"

    overall_ok = all(value == "ok" for value in checks.values())
    return {
        "status": "ok" if overall_ok else "degraded",
        "checks": checks,
    }


@app.post("/produtos/", response_model=schemas.ProductResponse, status_code=201)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    try:
        return actions.create_product(db, product)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Produto já registrado")


@app.get("/produtos/", response_model=list[schemas.ProductResponse])
def read_products(
        skip: int = 0, 
        limit: int = 100, 
        db: Session = Depends(get_db),  
    ):
    return actions.get_products(db, skip=skip, limit=limit)
