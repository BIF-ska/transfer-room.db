"""add columns to teams

Revision ID: b8111a1c7faf
Revises: dd0e0f17d196
Create Date: 2025-02-10 11:01:21.217835

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8111a1c7faf'
down_revision: Union[str, None] = 'dd0e0f17d196'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
      # Add columns country_id and competition_id to teams table
    op.add_column('teams', sa.Column('country_id', sa.Integer(), nullable=False))
    op.add_column('teams', sa.Column('competition_id', sa.Integer(), nullable=False))
    


def downgrade() -> None:
    op.drop_column('teams', 'country_id')
    op.drop_column('teams', 'competition_id')

