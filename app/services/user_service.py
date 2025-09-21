from typing import List, Optional
from datetime import datetime
from app.models.user import User, UserCreate

class UserService:
    # Simulierte Datenbank - in der Realität würde man eine echte DB verwenden
    _users_db = []
    _next_id = 1
    
    @classmethod
    def get_all_users(cls) -> List[User]:
        """Alle Benutzer abrufen"""
        return cls._users_db
    
    @classmethod
    def get_user_by_id(cls, user_id: int) -> Optional[User]:
        """Benutzer nach ID abrufen"""
        for user in cls._users_db:
            if user.id == user_id:
                return user
        return None
    
    @classmethod
    def create_user(cls, user_data: UserCreate) -> User:
        """Neuen Benutzer erstellen"""
        user = User(
            id=cls._next_id,
            email=user_data.email,
            name=user_data.name,
            is_active=user_data.is_active,
            created_at=datetime.now()
        )
        cls._users_db.append(user)
        cls._next_id += 1
        return user
    
    @classmethod
    def update_user(cls, user_id: int, user_data: UserCreate) -> Optional[User]:
        """Benutzer aktualisieren"""
        for i, user in enumerate(cls._users_db):
            if user.id == user_id:
                updated_user = User(
                    id=user.id,
                    email=user_data.email,
                    name=user_data.name,
                    is_active=user_data.is_active,
                    created_at=user.created_at,
                    updated_at=datetime.now()
                )
                cls._users_db[i] = updated_user
                return updated_user
        return None
    
    @classmethod
    def delete_user(cls, user_id: int) -> bool:
        """Benutzer löschen"""
        for i, user in enumerate(cls._users_db):
            if user.id == user_id:
                del cls._users_db[i]
                return True
        return False
