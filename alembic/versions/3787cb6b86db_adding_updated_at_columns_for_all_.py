"""adding updated at columns for all tables ,and adding rating column to player table

Revision ID: 3787cb6b86db
Revises: bcbe1205657b
Create Date: 2025-03-20 09:35:20.943561

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3787cb6b86db'
down_revision: Union[str, None] = 'bcbe1205657b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add 'rating' column with a default value to avoid NOT NULL errors
    op.add_column('players', sa.Column('rating', sa.Float(), nullable=False, server_default='0'))

    # Add 'updated_at' column with a default value to prevent NOT NULL issues
    op.add_column('players', sa.Column('updated_at', sa.Date, nullable=False, server_default=sa.text('GETDATE()')))
    op.add_column('team', sa.Column('updated_at', sa.Date, nullable=False, server_default=sa.text('GETDATE()')))
    op.add_column('agencies', sa.Column('updated_at', sa.Date, nullable=False, server_default=sa.text('GETDATE()')))
    op.add_column('competition', sa.Column('updated_at', sa.Date, nullable=False, server_default=sa.text('GETDATE()')))

def downgrade() -> None:
    op.drop_column('players', 'rating')
    op.drop_column('players', 'updated_at')
    op.drop_column('teams', 'updated_at')
    op.drop_column('countries', 'updated_at')
    op.drop_column('agencies', 'updated_at')
    op.drop_column('competition', 'updated_at')