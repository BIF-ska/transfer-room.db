"""adding columns to teams table

Revision ID: 96080642fd32
Revises: dd0e0f17d196
Create Date: 2025-02-10 08:50:47.011657

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96080642fd32'
down_revision: Union[str, None] = 'dd0e0f17d196'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
