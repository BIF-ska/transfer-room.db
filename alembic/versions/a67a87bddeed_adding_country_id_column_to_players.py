"""adding country_id column to players  

Revision ID: a67a87bddeed
Revises: 1adb926d18a8
Create Date: 2025-02-17 11:25:04.021893

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a67a87bddeed'
down_revision: Union[str, None] = '1adb926d18a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("Players", sa.Column("player_Country_id", sa.Integer(), nullable=False))
    op.create_foreign_key("player_Country_id", "Players", "Country", ["player_Country_id"], ["country_id"])




def downgrade() -> None:
    pass
