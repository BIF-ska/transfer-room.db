"""Merging multiple heads

Revision ID: b6831084a98f
Revises: ab4c3e1deee3, bcd76b5366c6
Create Date: 2025-02-13 10:40:27.518352

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6831084a98f'
down_revision: Union[str, None] = ('ab4c3e1deee3', 'bcd76b5366c6')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
