from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    quantity: int

items = {}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail={"error": "item_not_found", "message": "Item not found"})
    return items[item_id]

@app.post("/items/{item_id}")
def create_item(item_id: int, item: Item):
    items[item_id] = item
    return {"message": "created"}

@app.get("/items/{item_id}/total")
def get_total(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail={"error": "item_not_found", "message": "Item not found"})
    item = items[item_id]
    if item.quantity == 0:
        return {"total": 0, "quantity": 0, "message": "Out of stock"}
    price_per_unit = item.price / item.quantity
    return {"total": price_per_unit * item.quantity}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail={"error": "item_not_found", "message": "Item not found"})
    del items[item_id]
    return {"message": "Item deleted successfully"}
