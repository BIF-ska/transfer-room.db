"""addring rating,xtv to players table 

Revision ID: b4d014547038
Revises: bcbe1205657b
Create Date: 2025-04-01 10:11:30.040022

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4d014547038'
down_revision: Union[str, None] = 'bcbe1205657b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
        op.add_column('players', sa.Column('rating', sa.Numeric, nullable=True))
        op.add_column('players', sa.Column('xTV', sa.Numeric, nullable=True))


def downgrade() -> None:
    op.drop_column('players', 'rating')
    op.drop_column('players', 'xtv')

