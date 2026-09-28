"""Сущность «Жилец»."""
from typing import List


class Tenant:
    """Жилец - пользователь системы, подающий заявки."""

    def __init__(
        self,
        tenant_id: int,
        name: str,
        flat: int,
        phone: str = "",
    ) -> None:
        self.id = tenant_id
        self.name = name
        self.flat = flat
        self.phone = phone

    @classmethod
    def from_data(cls, data: dict) -> "Tenant":
        """Создать жильца из словаря JSON."""
        return cls(
            tenant_id=data["id"],
            name=data["name"],
            flat=data["flat"],
            phone=data.get("phone", ""),
        )

    def to_data(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "flat": self.flat,
            "phone": self.phone,
        }

    def __str__(self) -> str:
        return f"Жилец #{self.id}: {self.name} (кв. {self.flat})"


#  функции работы с коллекцией жильцов

def add_tenant(
    tenants: List[Tenant],
    name: str,
    flat: int,
    phone: str = "",
) -> Tenant:
    """Создать жильца и добавить его в коллекцию."""
    new_id = max((t.id for t in tenants), default=0) + 1
    tenant = Tenant(new_id, name, flat, phone)
    tenants.append(tenant)
    return tenant


def find_tenant_by_flat(tenants: List[Tenant], flat: int) -> List[Tenant]:
    """Найти всех жильцов по номеру квартиры."""
    return [t for t in tenants if t.flat == flat]


def find_tenant_by_id(tenants: List[Tenant], tenant_id: int):
    """Найти жильца по идентификатору."""
    for tenant in tenants:
        if tenant.id == tenant_id:
            return tenant
    return None


def show_tenants(tenants: List[Tenant]) -> None:
    """Вывести информацию обо всех жильцах."""
    if not tenants:
        print("Список жильцов пуст.")
        return
    for tenant in tenants:
        print(tenant)