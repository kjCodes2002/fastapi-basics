from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Product 
from database import engine, session
from sqlalchemy.orm import Session
import database_models
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"] 
)

database_models.Base.metadata.create_all(bind=engine)

@app.get('/')
def greet():
    return "Welcome Home!"

products = [
    Product(id=1, name="smartphone", description="Midrange smartphone", price=28999, quantity=78),
    Product(id=34, name='bracelet', description="Men's accessories", price=499, quantity=146)
]

def get_db():
    db = session()
    try:
        yield db
    finally: 
        db.close()

def db__init():
    db = session()
    count = db.query(database_models.Product).count()

    if count == 0:
        for product in products: 
            db.add(database_models.Product(**product.model_dump()))
        db.commit()
    
db__init()

@app.get('/products')
def get_all_products(db: Session = Depends(get_db)): #Depends() is to inject a dependency
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get('/product/{id}')
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    return "Product not found"

@app.post('/product')
def add_product(product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product.id).first()
    if db_product:
        return 'id already exists'
    else: 
        db.add(database_models.Product(**product.model_dump()))
        db.commit()
        return 'product added'
    
@app.put('/product/{id}')
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return 'Product updated'
    else:
        return "Product not found"
    
@app.delete('/product/{id}')
def delete_product(id: int, db:Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return 'Product deleted'
    else:
        return 'Product not found'