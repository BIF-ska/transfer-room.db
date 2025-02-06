"""change players column

Revision ID: 2d5994d68578
Revises: a347ea860781
Create Date: 2025-02-06 11:42:32.082638

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d5994d68578'
down_revision: Union[str, None] = 'a347ea860781'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add new column `Rating` to the Players table
    op.add_column('Players', sa.Column('Rating', sa.Integer))
    op.add_column('Playerhistory', sa.Column('Rating', sa.Integer))
    op.add_column('Players', sa.Column('Transfervalue', sa.Integer))
    op.add_column('Teams', sa.Column('Teamrating', sa.Integer))

def downgrade():
    # Remove the column if you need to roll back
    op.drop_column('Players', 'Rating')
    op.drop_column('Playerhistory', 'Rating')
    op.drop_column('Players', 'Transfervalue')
    op.drop_column('Teams', 'Teamrating')

