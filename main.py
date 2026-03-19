from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    quantity: int

items = {}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    # BUG 1: no check if item exists — raises KeyError instead of 404
    item = items.get(item_id)
    if item is None:
        return {"error": "Item not found"}, 404
    return item

@app.post("/items/{item_id}")
def create_item(item_id: int, item: Item):
    items[item_id] = item
    return {"message": "created"}

@app.get("/items/{item_id}/total")
def get_total(item_id: int):
    item = items.get(item_id)
    if item is None:
        return {"error": "Item not found"}, 404
    if item.quantity == 0:
        return {"error": "Quantity must be greater than 0"}, 400
    # BUG 2: divides by quantity — crashes with ZeroDivisionError if quantity is 0
    price_per_unit = item.price / item.quantity
    return {"total": price_per_unit * item.quantity}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    # BUG 3: deletes without checking existence, and returns nothing (should confirm)
    if item_id in items:
        del items[item_id]
        return {}, 204
    return {"error": "Item not found"}, 404
