"""add foreign key to headcoach

Revision ID: ab4c3e1deee3
Revises: cce2928c79cc
Create Date: 2025-02-11 12:55:12.677747

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab4c3e1deee3'
down_revision: Union[str, None] = 'cce2928c79cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   
    op.add_column("HeadCoach", sa.Column("fk_Head_Coach", sa.Integer(), nullable=True))

    # ✅ Step 4: Recreate the foreign key constraint
    op.create_foreign_key("fk_Head_Coach", "HeadCoach", "Agencies", ["fk_Head_Coach"], ["id"])


def downgrade() -> None:
    pass
    op.drop_column("HeadCoach", "fk_Head_Coach") 
