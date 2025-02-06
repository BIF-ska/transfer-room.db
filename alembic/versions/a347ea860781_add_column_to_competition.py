"""add column to competition

Revision ID: a347ea860781
Revises: cd640d0b95cc
Create Date: 2025-02-06 11:12:58.203359

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a347ea860781'
down_revision: Union[str, None] = 'cd640d0b95cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Add new column `divisionLevel`
    op.add_column('Competition', sa.Column('divisionLevel', sa.Integer))

def downgrade():
    # Remove the column if you need to roll back
    op.drop_column('Competition', 'divisionLevel')