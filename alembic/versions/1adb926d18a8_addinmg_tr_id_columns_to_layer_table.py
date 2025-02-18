"""addinmg tr_id columns to layer table  

Revision ID: 1adb926d18a8
Revises: 3a7cf77f0d93
Create Date: 2025-02-13 14:47:42.457380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1adb926d18a8'
down_revision: Union[str, None] = '3a7cf77f0d93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("Players", sa.Column("TR_ID", sa.Integer(), nullable=True))
    




def downgrade() -> None:
        op.drop_column("Players", "TR_ID")

