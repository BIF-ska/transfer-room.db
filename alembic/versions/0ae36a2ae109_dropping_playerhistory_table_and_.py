"""dropping playerhistory table and generating new 

Revision ID: 0ae36a2ae109
Revises: d033f55a27d4
Create Date: 2025-02-20 09:24:31.215672

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0ae36a2ae109'
down_revision: Union[str, None] = 'd033f55a27d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
