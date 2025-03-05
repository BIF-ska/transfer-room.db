"""adding column player nam eto team_history 

Revision ID: ba225f28add0
Revises: e8ba4b748e73
Create Date: 2025-03-05 12:43:00.217381

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba225f28add0'
down_revision: Union[str, None] = 'e8ba4b748e73'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('Team_History', sa.Column('name', sa.String(), nullable=False))



def downgrade() -> None:
    op.drop_column('Team_History', 'name')
