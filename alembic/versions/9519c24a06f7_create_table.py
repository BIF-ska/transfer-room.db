"""create_table

Revision ID: 9519c24a06f7
Revises: f7efd8452dc6
Create Date: 2025-02-04 09:07:05.621592

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9519c24a06f7'
down_revision: Union[str, None] = 'f7efd8452dc6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
