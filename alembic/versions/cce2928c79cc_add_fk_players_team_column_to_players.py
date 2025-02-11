"""Add fk_players_team column to Players

Revision ID: cce2928c79cc
Revises: 173f8c4ebf76
Create Date: 2025-02-11 11:19:36.273650

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cce2928c79cc'
down_revision: Union[str, None] = '173f8c4ebf76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    # ✅ Step 1: Drop the old foreign key constraint
    op.drop_constraint("fk_players_team", "Players", type_="foreignkey")

   
    # ✅ Step 3: Recreate the column properly
    op.add_column("Players", sa.Column("fk_players_team", sa.Integer(), nullable=True))

    # ✅ Step 4: Recreate the foreign key constraint
    op.create_foreign_key("fk_players_team", "Players", "Teams", ["fk_players_team"], ["Team_id"])


def downgrade() -> None:
    pass
