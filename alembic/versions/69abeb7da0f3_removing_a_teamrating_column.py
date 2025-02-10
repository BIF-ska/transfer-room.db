"""removing a teamRating column

Revision ID: 69abeb7da0f3
Revises: 0cb2c2f29925
Create Date: 2025-02-10 12:05:25.220447

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69abeb7da0f3'
down_revision: Union[str, None] = '0cb2c2f29925'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Remove the column from the table
    op.drop_column('Teams', 'Teamrating')

def downgrade():
    # Re-add the column in case of rollback
    op.add_column('Teams', sa.Column('Teamrating', sa.Integer(length=255), nullable=True))