"""REMOVING 2 columns from player metrics  

Revision ID: 38a7569f6568
Revises: 13a7505123ef
Create Date: 2025-03-05 10:02:58.224689

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38a7569f6568'
down_revision: Union[str, None] = '13a7505123ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Remove columns from the database
    with op.batch_alter_table('PlayerMetrics') as batch_op:
        batch_op.drop_column('MinutesPlayed')
        batch_op.drop_column('Salary')

def downgrade() -> None:
    # Add columns back in case we need to rollback
    with op.batch_alter_table('PlayerMetrics') as batch_op:
        batch_op.add_column(sa.Column('MinutesPlayed', sa.Numeric(18, 0), nullable=True))
        batch_op.add_column(sa.Column('Salary', sa.Numeric(18, 0), nullable=True))
