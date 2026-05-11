"""Update Product price to Decimal

Revision ID: 001
Revises: 
Create Date: 2026-05-11

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new column with NUMERIC type
    op.add_column('product', sa.Column('price_new', sa.Numeric(precision=10, scale=2), nullable=False, server_default='0.00'))
    
    # Copy data from old float column to new decimal column
    op.execute('UPDATE product SET price_new = price::numeric(10, 2)')
    
    # Drop old column
    op.drop_column('product', 'price')
    
    # Rename new column to price
    op.rename_table('product', 'product_temp')
    op.create_table(
        'product',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('stock', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('category_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.execute('''
        INSERT INTO product (id, name, description, price, stock, category_id)
        SELECT id, name, description, price_new, stock, category_id FROM product_temp
    ''')
    
    op.drop_table('product_temp')


def downgrade() -> None:
    # Convert back to float
    op.add_column('product', sa.Column('price_old', sa.Float(), nullable=False, server_default='0.0'))
    op.execute('UPDATE product SET price_old = price::float')
    op.drop_column('product', 'price')
    op.rename_table('product', 'product_temp')
    op.create_table(
        'product',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('stock', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('category_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.execute('''
        INSERT INTO product (id, name, description, price, stock, category_id)
        SELECT id, name, description, price_old, stock, category_id FROM product_temp
    ''')
    
    op.drop_table('product_temp')
