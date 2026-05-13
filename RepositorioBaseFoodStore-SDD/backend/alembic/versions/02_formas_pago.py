"""
Create formas_pago table and update orders

Revision ID: 02_formas_pago
Revises: 01_orders_init
Create Date: 2026-05-13
"""
from alembic import op
import sqlalchemy as sa

revision = '02_formas_pago'
down_revision = '01_orders_init'
branch_labels = None
depends_on = None

def upgrade():
    # Create formas_pago table
    op.create_table(
        'formas_pago',
        sa.Column('codigo', sa.String(20), primary_key=True, index=True),
        sa.Column('habilitado', sa.Boolean(), server_default='true', nullable=False),
    )
    
    # Add forma_pago_codigo to orders table
    op.add_column(
        'orders',
        sa.Column('forma_pago_codigo', sa.String(20), sa.ForeignKey('formas_pago.codigo'), nullable=True)
    )

def downgrade():
    # Remove forma_pago_codigo from orders table
    op.drop_constraint('fk_orders_forma_pago_codigo', 'orders', type_='foreignkey')
    op.drop_column('orders', 'forma_pago_codigo')
    
    # Drop formas_pago table
    op.drop_table('formas_pago')
