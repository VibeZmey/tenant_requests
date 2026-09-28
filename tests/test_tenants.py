from models import Tenant
from models.tenants import add_tenant, find_tenant_by_flat


def test_tenant_creation():
    tenant = Tenant(1, "Иванов И.И.", 101, "+7-900-000-00-00")
    assert tenant.id == 1
    assert tenant.name == "Иванов И.И."
    assert tenant.flat == 101


def test_tenant_str():
    tenant = Tenant(1, "Иванов И.И.", 101)
    assert "Иванов И.И." in str(tenant)
    assert "101" in str(tenant)


def test_add_tenant():
    tenants = []
    tenant = add_tenant(tenants, "Петров П.П.", 202)
    assert len(tenants) == 1
    assert tenant.id == 1
    assert tenant.flat == 202


def test_find_tenant_by_flat():
    tenants = [
        Tenant(1, "Иванов И.И.", 101),
        Tenant(2, "Петров П.П.", 102),
    ]
    found = find_tenant_by_flat(tenants, 101)
    assert len(found) == 1
    assert found[0].name == "Иванов И.И."