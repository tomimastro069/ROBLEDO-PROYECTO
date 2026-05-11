"""Add soft-delete support to Product model

Revision ID: 002
Revises: 001
Create Date: 2026-05-11

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add deleted_at column to product table (nullable, defaults to NULL)
    op.add_column('product', sa.Column('deleted_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    # Remove deleted_at column
    op.drop_column('product', 'deleted_at')
