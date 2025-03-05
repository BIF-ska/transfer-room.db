"""changingplayer history table adding-removing 

Revision ID: 04521eb72d4a
Revises: ba225f28add0
Create Date: 2025-03-05 12:54:40.532772

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04521eb72d4a'
down_revision: Union[str, None] = 'ba225f28add0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("PlayerHistory") as batch_op:
        # 🔥 Remove columns that are no longer needed
        batch_op.drop_column("Transfervalue")
        batch_op.drop_column("TeamID")

        # 🔥 Add new columns to match JSON format
        batch_op.add_column(sa.Column("year", sa.Integer, nullable=False))
        batch_op.add_column(sa.Column("month", sa.Integer, nullable=False))
        batch_op.add_column(sa.Column("xTV", sa.Numeric(18, 2), nullable=False))

def downgrade() -> None:
    with op.batch_alter_table("PlayerHistory") as batch_op:
        # 🔥 Remove newly added columns
        batch_op.drop_column("year")
        batch_op.drop_column("month")
        batch_op.drop_column("xTV")

        # 🔥 Restore old columns
        batch_op.add_column(sa.Column("Transfervalue", sa.Numeric(12, 2), nullable=True))