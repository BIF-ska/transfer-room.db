"""create_table

Revision ID: f7efd8452dc6
Revises: 
Create Date: 2025-02-03 13:22:23.621979

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7efd8452dc6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        'Country',
        sa.Column('Country_id', sa.Integer, primary_key=True),
        sa.Column('Name', sa.String),
    )

op.create_table(
        'Competition',
        sa.Column('Competition_id', sa.Integer, primary_key=True),
        sa.Column('Competitionname', sa.String),
    )

op.create_table(
        'Players',
        sa.Column('PlayerID', sa.Integer, primary_key=True),
        sa.Column('Name', sa.String(100)),
        sa.Column('BirthDate', sa.Date),
        sa.Column('FirstPosition', sa.String(100)),
        sa.Column('Nationality1', sa.String(100)),
        sa.Column('Nationality2', sa.String(100), nullable=True),
        sa.Column('ParentTeam', sa.String(100)),
    )



def downgrade() -> None:
    op.drop_table('Country')
    op.drop_table('Competition')
    op.drop_table('Players')