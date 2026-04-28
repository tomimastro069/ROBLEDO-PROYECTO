"""
Roles del sistema FoodStore.

5 actores definidos en el dominio:
  - cliente      → compra productos
  - admin        → gestión total del sistema
  - gestor_stock → gestión de inventario y productos
  - gestor_pedidos → gestión y seguimiento de pedidos
  - sistema      → procesos automatizados (ej: webhooks MercadoPago)
"""

from enum import Enum


class Role(str, Enum):
    CLIENTE = "cliente"
    ADMIN = "admin"
    GESTOR_STOCK = "gestor_stock"
    GESTOR_PEDIDOS = "gestor_pedidos"
    SISTEMA = "sistema"
