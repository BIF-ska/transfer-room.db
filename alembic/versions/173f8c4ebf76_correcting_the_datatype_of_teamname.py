"""correcting the datatype of teamname

Revision ID: 173f8c4ebf76
Revises: 69abeb7da0f3
Create Date: 2025-02-10 13:59:39.908603

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '173f8c4ebf76'
down_revision: Union[str, None] = '69abeb7da0f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    # Drop the existing 'Teamname' column from the 'teams' table.
    op.drop_column('teams', 'Teamname')
    
    # Recreate the 'Teamname' column as a String.
    # Adjust the length and nullability as needed.
    op.add_column('teams', sa.Column('Teamname', sa.String(length=100), nullable=True))


def downgrade() -> None:
    # To revert, drop the new 'Teamname' column.
    op.drop_column('teams', 'Teamname')
    
    # Re-add the original 'Teamname' column.
    # Adjust the definition to match the original schema if necessary.
    op.add_column('teams', sa.Column('Teamname', sa.String(length=100), nullable=True))