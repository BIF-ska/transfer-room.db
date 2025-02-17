"""Dropping PlayerHistory and recreating it 

Revision ID: 3a7cf77f0d93
Revises: b6831084a98f
Create Date: 2025-02-13 10:40:52.506442
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic
revision: str = "3a7cf77f0d93"
down_revision: Union[str, None] = "b6831084a98f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Drop the old PlayerHistory table and recreate it with the correct foreign keys."""

    # Drop the table if it exists
    op.drop_table("PlayerHistory", if_exists=True)

    # Recreate PlayerHistory table
    op.create_table(
        "PlayerHistory",
        sa.Column("HistoryID", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("PlayerID", sa.Integer, nullable=False),
        sa.Column("TeamID", sa.Integer, nullable=False),
        sa.Column("Name", sa.String(100), nullable=False),

        sa.Column("Rating", sa.Numeric(3, 1), nullable=True),
        sa.Column("Transfervalue", sa.Numeric(10, 2), nullable=True),
        sa.Column("UpdatedAt", sa.DateTime, server_default=sa.func.now(), nullable=False)
    )

    # ✅ Create Foreign Keys AFTER the table is created
    op.create_foreign_key(
        "fk_PlayerHistory_Player",  # Unique constraint name
        "PlayerHistory",  # Child table
        "Players",  # Parent table
        ["PlayerID"],  # Child table column
        ["PlayerID"],  # Parent table column
        ondelete="CASCADE"
    )

    op.create_foreign_key(
        "fk_PlayerHistory_Team",  # Unique constraint name
        "PlayerHistory",  # Child table
        "Teams",  # Parent table
        ["TeamID"],  # Child table column
        ["Team_id"],  # Parent table column
        ondelete="CASCADE"
    )

def downgrade() -> None:
    """Rollback changes: Drop the new PlayerHistory table."""
    op.drop_table("PlayerHistory")
