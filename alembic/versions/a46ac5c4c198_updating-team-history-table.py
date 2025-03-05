"""updarting team history table 

Revision ID: a46ac5c4c198
Revises: 38a7569f6568
Create Date: 2025-03-05 10:30:11.290031

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a46ac5c4c198'
down_revision: Union[str, None] = '38a7569f6568'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop old columns
    with op.batch_alter_table("Team_History") as batch_op:
        batch_op.drop_column("year")
        batch_op.drop_column("month")
        batch_op.drop_column("xTV")

    # Add new columns with the correct types
    with op.batch_alter_table("Team_History") as batch_op:
        batch_op.add_column(sa.Column("from_team_id", sa.Integer, nullable=False))
        batch_op.add_column(sa.Column("from_team", sa.String(255), nullable=False))
        batch_op.add_column(sa.Column("to_team_id", sa.Integer, nullable=False))
        batch_op.add_column(sa.Column("to_team", sa.String(255), nullable=False))
        batch_op.add_column(sa.Column("start_date", sa.Date, nullable=False))
        batch_op.add_column(sa.Column("end_date", sa.Date, nullable=True))  # Nullable because end date might be empty
        batch_op.add_column(sa.Column("transfer_type", sa.String(50), nullable=False))
        batch_op.add_column(sa.Column("transfer_fee_euros", sa.Numeric(18, 2), nullable=False, default=0))
        # ✅ Use DATETIME2 instead of TIMESTAMP
        batch_op.add_column(sa.Column("created_at", sa.DateTime, server_default=sa.func.getdate(), nullable=False))

def downgrade() -> None:
    # Revert changes
    with op.batch_alter_table("Team_History") as batch_op:
        batch_op.drop_column("from_team_id")
        batch_op.drop_column("from_team")
        batch_op.drop_column("to_team_id")
        batch_op.drop_column("to_team")
        batch_op.drop_column("start_date")
        batch_op.drop_column("end_date")
        batch_op.drop_column("transfer_type")
        batch_op.drop_column("transfer_fee_euros")
        batch_op.drop_column("created_at")

    # Restore old columns
    with op.batch_alter_table("Team_History") as batch_op:
        batch_op.add_column(sa.Column("year", sa.Integer, nullable=False))
        batch_op.add_column(sa.Column("month", sa.Integer, nullable=False))
        batch_op.add_column(sa.Column("xTV", sa.Numeric(18, 2), nullable=False))