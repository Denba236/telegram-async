from typing import Dict, Optional, Union, List
from enum import Enum


class Roles:
    """Stałe dla ról użytkowników"""
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    GUEST = "guest"

    @classmethod
    def all(cls) -> List[str]:
        """Zwraca listę wszystkich dostępnych ról"""
        return [cls.ADMIN, cls.MODERATOR, cls.USER, cls.GUEST]

    @classmethod
    def hierarchy(cls) -> Dict[str, int]:
        """Zwraca hierarchię ról (wyższa liczba = wyższa ranga)"""
        return {
            cls.ADMIN: 100,
            cls.MODERATOR: 50,
            cls.USER: 10,
            cls.GUEST: 0
        }


class RoleManager:
    """
    Menedżer ról użytkowników

    Przykład:
        roles = RoleManager()
        roles.set_role(123456, Roles.ADMIN)

        @dp.message()
        @role_required(Roles.MODERATOR)
        async def admin_only(ctx):
            pass
    """

    def __init__(self):
        self.user_roles: Dict[int, str] = {}

    def set_role(self, user_id: int, role: str):
        """Ustawia rolę dla użytkownika"""
        if role not in Roles.all():
            raise ValueError(f"Invalid role: {role}. Available: {Roles.all()}")
        self.user_roles[user_id] = role

    def get_role(self, user_id: int) -> str:
        """Zwraca rolę użytkownika (domyślnie USER)"""
        return self.user_roles.get(user_id, Roles.USER)

    def has_role(self, user_id: int, required_role: str) -> bool:
        """
        Sprawdza czy użytkownik ma wymaganą rolę (uwzględnia hierarchię)
        """
        user_role = self.get_role(user_id)
        hierarchy = Roles.hierarchy()

        user_level = hierarchy.get(user_role, 0)
        required_level = hierarchy.get(required_role, 0)

        return user_level >= required_level

    def remove_role(self, user_id: int):
        """Usuwa rolę użytkownika (przywraca USER)"""
        if user_id in self.user_roles:
            del self.user_roles[user_id]

    def get_users_by_role(self, role: str) -> List[int]:
        """Zwraca listę użytkowników z daną rolą"""
        return [uid for uid, r in self.user_roles.items() if r == role]

    def clear(self):
        """Czyści wszystkie role"""
        self.user_roles.clear()


# Dekorator do sprawdzania ról
def role_required(required_role: str):
    """
    Dekorator wymagający odpowiedniej roli

    Przykład:
        @dp.message(Command("admin"))
        @role_required(Roles.ADMIN)
        async def admin_panel(ctx):
            await ctx.reply("Panel administratora")
    """

    def decorator(func):
        async def wrapper(ctx, *args, **kwargs):
            # Role manager powinien być dostępny przez ctx lub jako zmienna globalna
            # To jest uproszczona wersja
            if hasattr(ctx, 'role_manager'):
                role_manager = ctx.role_manager
            else:
                # Fallback - brak role managera
                return await func(ctx, *args, **kwargs)

            if role_manager.has_role(ctx.user_id, required_role):
                return await func(ctx, *args, **kwargs)
            else:
                await ctx.reply("❌ Nie masz uprawnień do tej komendy.")
                return None

        return wrapper

    return decorator