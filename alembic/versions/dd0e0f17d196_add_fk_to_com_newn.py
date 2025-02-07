"""add fk to com newn

Revision ID: dd0e0f17d196
Revises: 3115ba43cd23
Create Date: 2025-02-07 15:26:55.042653

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd0e0f17d196'
down_revision: Union[str, None] = '3115ba43cd23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   op.create_foreign_key(
    "fk_competition_country",  # Constraint name
    "Competition",             # Source table (the table that contains the foreign key)
    "Country",                 # Referenced table (the table with the primary key)
    ["country_fk_id"],            # Local column in Competition
    ["Country_id"]             # Referenced column in Country
)

def downgrade() -> None:
    pass
