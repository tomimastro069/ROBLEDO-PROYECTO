"""merge_multiple_heads

Revision ID: 35f529171d3a
Revises: 001_initial, 002
Create Date: 2026-05-13 20:39:45.819405

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '35f529171d3a'
down_revision: Union[str, Sequence[str], None] = ('001_initial', '002')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
