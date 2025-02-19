"""Merging multiple heads and creating PlayerAgency table

Revision ID: d033f55a27d4
Revises: a67a87bddeed, d8559da4b381
Create Date: 2025-02-19 12:59:23.662076

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'd033f55a27d4'
down_revision: Union[str, None] = ('a67a87bddeed', 'd8559da4b381')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create the PlayerAgency table
    op.create_table(
        "PlayerAgency",
        sa.Column("player_id", sa.Integer, primary_key=True),
        sa.Column("agency_id", sa.Integer, primary_key=True)
    )

    # Add foreign keys separately
    op.create_foreign_key("fk_player_id", "PlayerAgency", "Players", ["player_id"], ["PlayerID"])
    op.create_foreign_key("fk_agency_id", "PlayerAgency", "Agencies", ["agency_id"], ["id"])


def downgrade() -> None:
    # Drop foreign keys first
    op.drop_constraint("fk_player_id", "PlayerAgency", type_="foreignkey")
    op.drop_constraint("fk_agency_id", "PlayerAgency", type_="foreignkey")
    
    # Drop the PlayerAgency table
    op.drop_table("PlayerAgency")
