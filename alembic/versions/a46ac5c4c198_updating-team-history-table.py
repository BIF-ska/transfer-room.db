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

    # Add new columns (without from_team_id & to_team_id)
    with op.batch_alter_table("Team_History") as batch_op:
        batch_op.add_column(sa.Column("from_team", sa.String(255), nullable=False))
        batch_op.add_column(sa.Column("to_team", sa.String(255), nullable=False))
        batch_op.add_column(sa.Column("start_date", sa.Date, nullable=False))
        batch_op.add_column(sa.Column("end_date", sa.Date, nullable=True))  # Nullable because end date might be empty
        batch_op.add_column(sa.Column("transfer_type", sa.String(50), nullable=False))
        batch_op.add_column(sa.Column("transfer_fee_euros", sa.Numeric(18, 2), nullable=False, default=0))
        # ✅ Use DATETIME2 instead of TIMESTAMP
        batch_op.add_column(sa.Column("created_at", sa.DateTime, server_default=sa.func.getdate(), nullable=False))


def downgrade() -> None:
    connection = op.get_bind()

    # 🔥 Step 1: Find the Default Constraint on `created_at`
    result = connection.execute("""
        SELECT name FROM sys.default_constraints 
        WHERE parent_object_id = OBJECT_ID('Team_History') 
        AND parent_column_id = COLUMNPROPERTY(OBJECT_ID('Team_History'), 'created_at', 'ColumnId')
    """)
    constraint_name = result.scalar()

    # 🔥 Step 2: Drop the Default Constraint if It Exists
    if constraint_name:
        connection.execute(f"ALTER TABLE Team_History DROP CONSTRAINT {constraint_name}")

    # 🔥 Step 3: Now Drop the `created_at` Column
    with op.batch_alter_table("Team_History") as batch_op:
        batch_op.drop_column("created_at")
        batch_op.drop_column("from_team")
        batch_op.drop_column("to_team")
        batch_op.drop_column("start_date")
        batch_op.drop_column("end_date")
        batch_op.drop_column("transfer_type")
        batch_op.drop_column("transfer_fee_euros")

    # 🔥 Step 4: Restore the Old Columns
    with op.batch_alter_table("Team_History") as batch_op:
        batch_op.add_column(sa.Column("year", sa.Integer, nullable=False))
        batch_op.add_column(sa.Column("month", sa.Integer, nullable=False))
        batch_op.add_column(sa.Column("xTV", sa.Numeric(18, 2), nullable=False))

    print("Successfully downgraded Team_History table.")

