from fastapi import FastAPI
from models import Product 
app = FastAPI()

@app.get('/')
def greet():
    return "Welcome Home!"

products = [
    Product(id=1, name="smartphone", description="Midrange smartphone", price=28999, quantity=78),
    Product(id=34, name='bracelet', description="Men's accessories", price=499, quantity=146)
]
@app.get('/products')
def get_all_products():
    return products

@app.get('/product/{id}')
def get_product_by_id(id: int):
    for product in products:
        if product.id == id:
            return product
    return "Couldn't find product"

@app.post('/product')
def add_product(product: Product):
    products.append(product)
    return product