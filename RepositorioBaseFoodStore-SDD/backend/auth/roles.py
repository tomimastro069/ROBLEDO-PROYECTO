"""
Roles del sistema FoodStore.

4 actores definidos en el dominio:
  - cliente      → compra productos
  - admin        → gestión total del sistema
  - gestor_stock → gestión de inventario y productos
  - gestor_pedidos → gestión y seguimiento de pedidos
"""

from enum import Enum


class Role(str, Enum):
    CLIENTE = "cliente"
    ADMIN = "admin"
    GESTOR_STOCK = "gestor_stock"
    GESTOR_PEDIDOS = "gestor_pedidos"
