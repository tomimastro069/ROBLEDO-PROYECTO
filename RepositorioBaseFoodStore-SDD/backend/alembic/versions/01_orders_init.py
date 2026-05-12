"""
Create orders and order_items tables

Revision ID: 01_orders_init
Revises: 
Create Date: 2026-05-11
"""
from alembic import op
import sqlalchemy as sa

revision = '01_orders_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False, index=True),
        sa.Column('status', sa.String(16), nullable=False, index=True),
        sa.Column('total', sa.Float, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), index=True),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    op.create_table(
        'order_items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('order_id', sa.Integer, sa.ForeignKey('orders.id'), index=True),
        sa.Column('product_id', sa.Integer, nullable=False, index=True),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('price', sa.Float, nullable=False),
    )
    op.create_index('ix_orders_user_id', 'orders', ['user_id'])
    op.create_index('ix_orders_status', 'orders', ['status'])
    op.create_index('ix_orders_created_at', 'orders', ['created_at'])
    op.create_index('ix_order_items_order_id', 'order_items', ['order_id'])
    op.create_index('ix_order_items_product_id', 'order_items', ['product_id'])

def downgrade():
    op.drop_index('ix_order_items_product_id', table_name='order_items')
    op.drop_index('ix_order_items_order_id', table_name='order_items')
    op.drop_index('ix_orders_created_at', table_name='orders')
    op.drop_index('ix_orders_status', table_name='orders')
    op.drop_index('ix_orders_user_id', table_name='orders')
    op.drop_table('order_items')
    op.drop_table('orders')
