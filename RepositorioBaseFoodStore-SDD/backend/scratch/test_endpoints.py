import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def get_token(email, password):
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": email, "password": password}
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

def test_endpoints():
    print("--- INICIANDO TEST INTEGRAL DE ENDPOINTS ---\n")
    
    # 1. Login
    admin_token = get_token("admin@foodstore.local", "admin123")
    cliente_token = get_token("cliente@test.com", "cliente123")
    
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    cliente_headers = {"Authorization": f"Bearer {cliente_token}"}
    
    if not admin_token or not cliente_token:
        print("❌ Error en el login.")
        return

    print("✅ Login exitoso para Admin y Cliente.")

    # 2. Categorías (Público)
    resp = requests.get(f"{BASE_URL}/categories")
    if resp.status_code == 200:
        print(f"✅ [Categorías]: OK ({len(resp.json())} encontradas)")
    
    # 3. Productos (Público)
    resp = requests.get(f"{BASE_URL}/products")
    if resp.status_code == 200:
        print(f"✅ [Productos]: OK ({len(resp.json()['items'])} encontrados)")

    # 4. Perfil (Privado)
    resp = requests.get(f"{BASE_URL}/perfil/me", headers=cliente_headers)
    if resp.status_code == 200:
        print(f"✅ [Perfil Cliente]: OK (Nombre: {resp.json().get('name')})")

    # 5. Direcciones (Privado)
    resp = requests.get(f"{BASE_URL}/direcciones", headers=cliente_headers)
    address_id = None
    if resp.status_code == 200:
        direcciones = resp.json()
        print(f"✅ [Direcciones]: OK ({len(direcciones)} encontradas)")
        if direcciones:
            address_id = direcciones[0]["id"]
            print(f"   - Dirección actual: {direcciones[0]['street']} {direcciones[0]['numero']}")

    # 6. Órdenes - Listar
    resp = requests.get(f"{BASE_URL}/orders", headers=cliente_headers)
    if resp.status_code == 200:
        print(f"✅ [Órdenes Cliente]: OK ({len(resp.json())} pedidos encontrados)")

    # 7. Órdenes - Crear (Test de estrés/lógica)
    if address_id:
        new_order = {
            "items": [
                {"product_id": 1, "quantity": 2}
            ],
            "shipping_address_id": address_id
        }
        resp = requests.post(f"{BASE_URL}/orders/", json=new_order, headers=cliente_headers)
        if resp.status_code == 201:
            print(f"✅ [Crear Orden]: OK (ID: {resp.json()['id']})")
        else:
            print(f"⚠️ [Crear Orden]: Falló o requiere ajustes ({resp.status_code}) - {resp.text}")

    # 8. Admin - Dashboard
    resp = requests.get(f"{BASE_URL}/orders/admin/orders", headers=admin_headers)
    if resp.status_code == 200:
        print(f"✅ [Admin Orders]: OK ({len(resp.json())} pedidos totales en sistema)")
    else:
        print(f"❌ [Admin Orders]: Falló ({resp.status_code})")

    print("\n--- TEST INTEGRAL FINALIZADO ---")

if __name__ == "__main__":
    test_endpoints()
