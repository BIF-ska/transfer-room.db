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
        'Agencies',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('Agencyname', sa.String),
        sa.Column('Agencyverified', sa.Boolean),
    )

    op.create_table(
        'Competition',
        sa.Column('Competition_id', sa.Integer, primary_key=True),
        sa.Column('Competitionname', sa.String),
        sa.Column('Country_id', sa.Integer, sa.ForeignKey('Country.id')),
    )

    op.create_table(
        'Country',
        sa.Column('Country_id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
    )

    op.create_table(
        'Playeragencies',
        sa.Column('Agency_id', sa.Integer, sa.ForeignKey('Agencies.id')),
        sa.Column('Player_id', sa.String, sa.ForeignKey('Player.id')),
    )

    op.create_table(
        'Teams',
        sa.Column('Team_id', sa.String, primary_key=True),
        sa.Column('Teamname', sa.String),
        sa.Column('Competition_id', sa.Integer, sa.ForeignKey('Competition.Competition_id')),
        sa.Column('Country_id', sa.Integer, sa.ForeignKey('Country.id')),
    )

    op.create_table(
        'Playerhistory',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('Player_id', sa.String, primary_key=True),
        sa.Column('Team_id', sa.String, sa.ForeignKey('Teams.Team_id')),
        sa.Column('startdate', sa.DateTime),
        sa.Column('enddate', sa.DateTime),
        sa.Column('Timestamp', sa.DateTime),
        sa.Column('Transfervalue', sa.Float),
        sa.Column('last_updated', sa.DateTime),
        sa.Column('create', sa.DateTime),
        sa.Column('update', sa.DateTime),

    )


def downgrade() -> None:
    op.drop_table('Agencies')
    op.drop_table('Competition')
    op.drop_table('Country')
    op.drop_table('Playeragencies')
    op.drop_table('Teams')
    op.drop_table('Playerhistory')