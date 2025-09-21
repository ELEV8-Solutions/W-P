from fastapi import APIRouter, HTTPException
from typing import List
from app.models.item import Item, ItemCreate
from app.services.item_service import ItemService

router = APIRouter()

@router.get("/", response_model=List[Item])
async def get_items():
    """Alle Items abrufen"""
    return ItemService.get_all_items()

@router.post("/", response_model=Item)
async def create_item(item: ItemCreate):
    """Neues Item erstellen"""
    return ItemService.create_item(item)

@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """Einzelnes Item abrufen"""
    item = ItemService.get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item nicht gefunden")
    return item

@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemCreate):
    """Item aktualisieren"""
    updated_item = ItemService.update_item(item_id, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item nicht gefunden")
    return updated_item

@router.delete("/{item_id}")
async def delete_item(item_id: int):
    """Item löschen"""
    success = ItemService.delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item nicht gefunden")
    return {"message": "Item erfolgreich gelöscht"}
