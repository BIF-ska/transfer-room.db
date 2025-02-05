"""Create foreign keys between tables

Revision ID: cd640d0b95cc
Revises: f7efd8452dc6
Create Date: 2025-02-05 09:24:58.097495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd640d0b95cc'
down_revision: Union[str, None] = 'f7efd8452dc6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass




def downgrade() -> None:
    pass
