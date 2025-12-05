from pydantic import BaseModel

#Recibe datos de producto nuevo
class CreateProduct(BaseModel):
    name : str
    price : float
    stock : int
    
#Respuesta
class Product(CreateProduct):
    id: int
    
    class Config:
        orm_mode = True