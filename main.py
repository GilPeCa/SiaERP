from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import SesionLocal, engine

# Crear tablas en la DB si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependencia para conectar a la DB
def get_db():
    db = SesionLocal()
    try:
        yield db
    finally:
        db.close()

# Rutas generales

@app.get("/ping")
def pong():
    return {"message": "pong"}

@app.get("/")
def read_root():
    return {"message": "API activa: raiz cha"}

#crud
# obtener todos los productos
@app.get("/products", response_model=List[schemas.Product])
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

#Crear nuevo producto
@app.post("/products", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(
        name=product.name, 
        price=product.price, 
        stock=product.stock
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

#actualizacion de stock 
@app.put("/products/{id}/stock")
def update_stock(id: int, quantity: int, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    
    if not db_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # act de la cantidad
    db_product.stock += quantity
    
    db.commit()
    return {"message": "Stock actualizado", "new_stock": db_product.stock}


#lov4cha