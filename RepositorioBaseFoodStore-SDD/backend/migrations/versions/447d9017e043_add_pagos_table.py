"""add_pagos_table

Revision ID: 447d9017e043
Revises: 35f529171d3a
Create Date: 2026-05-13 20:41:22.451985

Rollback:
    alembic downgrade 35f529171d3a
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '447d9017e043'
down_revision: Union[str, Sequence[str], None] = '35f529171d3a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'pagos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('pedido_id', sa.Integer(), nullable=False),
        sa.Column('preference_id', sa.String(), nullable=True),
        sa.Column('payment_id', sa.String(), nullable=True),
        sa.Column('idempotency_key', sa.String(), nullable=False),
        sa.Column('mp_status', sa.String(), nullable=False, server_default='pending'),
        sa.Column('mp_status_detail', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['pedido_id'], ['orders.id'], name='pagos_pedido_id_fkey'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('idempotency_key', name='pagos_idempotency_key_key'),
        sa.UniqueConstraint('payment_id', name='pagos_payment_id_key'),
    )
    op.create_index('ix_pagos_id', 'pagos', ['id'])
    op.create_index('ix_pagos_pedido_id', 'pagos', ['pedido_id'])
    op.create_index('ix_pagos_mp_status', 'pagos', ['mp_status'])
    op.create_index('ix_pagos_idempotency_key', 'pagos', ['idempotency_key'])
    op.create_index('ix_pagos_payment_id', 'pagos', ['payment_id'])
    op.create_index('ix_pagos_preference_id', 'pagos', ['preference_id'])


def downgrade() -> None:
    op.drop_index('ix_pagos_preference_id', table_name='pagos')
    op.drop_index('ix_pagos_payment_id', table_name='pagos')
    op.drop_index('ix_pagos_idempotency_key', table_name='pagos')
    op.drop_index('ix_pagos_mp_status', table_name='pagos')
    op.drop_index('ix_pagos_pedido_id', table_name='pagos')
    op.drop_index('ix_pagos_id', table_name='pagos')
    op.drop_table('pagos')
