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
    'Players',
    sa.Column('PlayerID', sa.Integer, primary_key=True),
    sa.Column('Name', sa.String(100), nullable=False),
    sa.Column('BirthDate', sa.Date),
    sa.Column('FirstPosition', sa.String(100)),
    sa.Column('Nationality1', sa.String(100)),
    sa.Column('Nationality2', sa.String(100), nullable=True),
    sa.Column('CurrentTeamID', sa.Integer, sa.ForeignKey('teams.TeamID')),
    sa.Column('ParentTeam', sa.String(100)),
    sa.Column('CompetitionID', sa.Integer, sa.ForeignKey('competition.CompetitionID')),
    sa.Column('TeamID', sa.Integer, sa.ForeignKey('teams.TeamID'))
    )

    op.create_table(
    'PlayerMetrics',
    sa.Column('MetricsID', sa.Integer, primary_key=True),
    sa.Column('PlayerID', sa.Integer, sa.ForeignKey('players.PlayerID')),
    sa.Column('Salary', sa.Numeric),  # Decimal maps to Numeric in SQLAlchemy
    sa.Column('ContractExpiry', sa.Date),
    sa.Column('PlayingStyle', sa.String(100)),
    sa.Column('xTV', sa.Numeric),
    sa.Column('PlayerRating', sa.Numeric),
    sa.Column('PlayerPotential', sa.Numeric),
    sa.Column('GBEStatus', sa.String(100)),
    sa.Column('MinutesPlayed', sa.Numeric)
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



    op.create_table(
        'Agencies',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('Agencyname', sa.String),
        sa.Column('Agencyverified', sa.Boolean),
    )

    op.create_table(
        'Playeragencies',
        sa.Column('Agency_id', sa.Integer, sa.ForeignKey('Agencies.id')),
        sa.Column('Player_id', sa.String, sa.ForeignKey('Player.id')),
    )

    op.create_table(
        'Country',
        sa.Column('Country_id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
    )



    op.create_table(
        'Competition',
        sa.Column('Competition_id', sa.Integer, primary_key=True),
        sa.Column('Competitionname', sa.String),
        sa.Column('Country_id', sa.Integer, sa.ForeignKey('Country.id')),
    )



    op.create_table(
        'Teams',
        sa.Column('Team_id', sa.String, primary_key=True),
        sa.Column('Teamname', sa.String),
        sa.Column('Competition_id', sa.Integer, sa.ForeignKey('Competition.Competition_id')),
        sa.Column('Country_id', sa.Integer, sa.ForeignKey('Country.id')),
    )

    op.create_table(
    'HeadCoach',
    sa.Column('CoachID', sa.Integer, primary_key=True),
    sa.Column('Name', sa.String(100), nullable=False),
    sa.Column('BirthDate', sa.Date),
    sa.Column('Nationality1', sa.String(100)),
    sa.Column('Nationality2', sa.String(100), nullable=True),
    sa.Column('CurrentTeamID', sa.Integer, sa.ForeignKey('teams.TeamID')),
    sa.Column('CurrentRole', sa.String(100)),
    sa.Column('ContractExpiry', sa.Date),
    sa.Column('AgencyID', sa.Integer, sa.ForeignKey('agencies.AgencyID'))
    )

    op.create_table(
    'TeamHistory',
    sa.Column('TeamHistory_ID', sa.Integer, primary_key=True),
    sa.Column('PlayerID', sa.Integer, sa.ForeignKey('players.PlayerID')),
    sa.Column('TeamID', sa.Integer, sa.ForeignKey('teams.TeamID')),
    sa.Column('StartDate', sa.Date),
    sa.Column('EndDate', sa.Date),
    sa.Column('EntityType', sa.Enum('Player', 'Coach', name='entity_type_enum'))
    )

op.create_table(
    'CoachMetrics',
    sa.Column('MetricID', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('CoachID', sa.Integer, sa.ForeignKey('HeadCoach.CoachID')),
    sa.Column('Rating', sa.Numeric),
    sa.Column('TacticalStyle', sa.String(100)),
    sa.Column('RatingChange12M', sa.Numeric),
    sa.Column('Suitability', sa.Numeric),
    sa.Column('TeamRatingImpact', sa.Numeric),
    sa.Column('TrustInYouth', sa.Numeric),
    sa.Column('PreferredFormation', sa.String(100)),
    sa.Column('SquadRotation', sa.Numeric),
    sa.Column('AvgTransferSpend', sa.Numeric)
    )




def downgrade() -> None:
    op.drop_table('Player')
    op.drop_table('PlayerMetrics')
    op.drop_table('Playerhistory')
    op.drop_table('Agencies')
    op.drop_table('Playeragencies')
    op.drop_table('Country')
    op.drop_table('Competition')
    op.drop_table('Teams')
    op.drop_table('HeadCoach')
    op.drop_table('TeamHistory')
    op.drop_table('CoachMetrics')