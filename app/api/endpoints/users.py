from fastapi import APIRouter, HTTPException
from typing import List
from app.models.user import User, UserCreate
from app.services.user_service import UserService

router = APIRouter()

@router.get("/", response_model=List[User])
async def get_users():
    """Alle Benutzer abrufen"""
    return UserService.get_all_users()

@router.post("/", response_model=User)
async def create_user(user: UserCreate):
    """Neuen Benutzer erstellen"""
    return UserService.create_user(user)

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Einzelnen Benutzer abrufen"""
    user = UserService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")
    return user

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserCreate):
    """Benutzer aktualisieren"""
    updated_user = UserService.update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")
    return updated_user

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    """Benutzer löschen"""
    success = UserService.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Benutzer nicht gefunden")
    return {"message": "Benutzer erfolgreich gelöscht"}
