"""adding Tr_id to Competiotn table  

Revision ID: 13a7505123ef
Revises: 0ae36a2ae109
Create Date: 2025-03-04 10:26:04.960682

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '13a7505123ef'
down_revision: Union[str, None] = '0ae36a2ae109'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
def upgrade():
    # Step 1: Add the column as nullable
    op.add_column("Competition", sa.Column("TR_com_ID", sa.Integer(), nullable=True))

    # Step 2: Set a default value (if needed) for existing rows
    op.execute("UPDATE Competition SET TR_com_ID = 0")  # or another meaningful default

    # Step 3: Make the column non-nullable after setting a default
    op.alter_column("Competition", "TR_com_ID", nullable=False)

def downgrade():
    op.drop_column("Competition", "TR_com_ID")
