"""changing data type in playermetrics estimated salry to string 

Revision ID: bcbe1205657b
Revises: 49281ce8c2d4
Create Date: 2025-03-12 14:25:23.446334

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bcbe1205657b'
down_revision: Union[str, None] = '49281ce8c2d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Change estimated_salary from Numeric(18,0) to String (VARCHAR 50)"""
    with op.batch_alter_table("player_metrics") as batch_op:
        batch_op.alter_column("estimated_salary",
                              existing_type=sa.Numeric(18, 0),
                              type_=sa.String(50),
                              nullable=True)


def downgrade() -> None:
    """Revert estimated_salary back to Numeric(18,0)"""
    with op.batch_alter_table("player_metrics") as batch_op:
        batch_op.alter_column("estimated_salary",
                              existing_type=sa.String(50),
                              type_=sa.Numeric(18, 0),
                              nullable=True)
