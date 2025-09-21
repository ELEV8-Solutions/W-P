from typing import List, Optional
from datetime import datetime
from app.models.item import Item, ItemCreate

class ItemService:
    # Simulierte Datenbank - in der Realität würde man eine echte DB verwenden
    _items_db = []
    _next_id = 1
    
    @classmethod
    def get_all_items(cls) -> List[Item]:
        """Alle Items abrufen"""
        return cls._items_db
    
    @classmethod
    def get_item_by_id(cls, item_id: int) -> Optional[Item]:
        """Item nach ID abrufen"""
        for item in cls._items_db:
            if item.id == item_id:
                return item
        return None
    
    @classmethod
    def create_item(cls, item_data: ItemCreate) -> Item:
        """Neues Item erstellen"""
        item = Item(
            id=cls._next_id,
            title=item_data.title,
            description=item_data.description,
            price=item_data.price,
            is_available=item_data.is_available,
            owner_id=1,  # Für Demo - normalerweise aus Authentication
            created_at=datetime.now()
        )
        cls._items_db.append(item)
        cls._next_id += 1
        return item
    
    @classmethod
    def update_item(cls, item_id: int, item_data: ItemCreate) -> Optional[Item]:
        """Item aktualisieren"""
        for i, item in enumerate(cls._items_db):
            if item.id == item_id:
                updated_item = Item(
                    id=item.id,
                    title=item_data.title,
                    description=item_data.description,
                    price=item_data.price,
                    is_available=item_data.is_available,
                    owner_id=item.owner_id,
                    created_at=item.created_at,
                    updated_at=datetime.now()
                )
                cls._items_db[i] = updated_item
                return updated_item
        return None
    
    @classmethod
    def delete_item(cls, item_id: int) -> bool:
        """Item löschen"""
        for i, item in enumerate(cls._items_db):
            if item.id == item_id:
                del cls._items_db[i]
                return True
        return False
