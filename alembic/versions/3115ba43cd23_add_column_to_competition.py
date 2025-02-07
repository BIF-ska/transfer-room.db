"""add column to competition

Revision ID: 3115ba43cd23
Revises: 2d5994d68578
Create Date: 2025-02-07 15:24:14.581257

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3115ba43cd23'
down_revision: Union[str, None] = '2d5994d68578'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column('competition', sa.Column('country_fk_id', sa.Integer))

def downgrade() -> None:
    pass
