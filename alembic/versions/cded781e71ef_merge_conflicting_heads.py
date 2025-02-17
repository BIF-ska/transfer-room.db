"""Merge conflicting heads

Revision ID: cded781e71ef
Revises: ab4c3e1deee3, bcd76b5366c6
Create Date: 2025-02-14 11:36:56.161386

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cded781e71ef'
down_revision: Union[str, None] = ('ab4c3e1deee3', 'bcd76b5366c6')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
