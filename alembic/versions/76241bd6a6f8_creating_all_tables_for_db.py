"""creating all tables for db 

Revision ID: 76241bd6a6f8
Revises: 
Create Date: 2025-03-06 11:34:08.775714

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76241bd6a6f8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
    'country',
    sa.Column('country_id', sa.Integer, primary_key=True,autoincrement=True),
    sa.Column('country_name', sa.String),
    )

    op.create_table(
    'competition',
    sa.Column('competition_id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('tr_id', sa.Integer, nullable=False),
    sa.Column('competition_name', sa.String, nullable=False),
    sa.Column('division_level', sa.Integer, nullable=False),
    sa.Column('country_id', sa.Integer, nullable=False),
    

    )

    op.create_table(
    'players',
    sa.Column('player_id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('tr_id', sa.Integer, nullable=False),
    sa.Column('competition_id', sa.Integer,nullable=False),
    sa.Column('player_name', sa.String(100), nullable=False),
    sa.Column('birth_date', sa.Date),
    sa.Column('first_position', sa.String(100)),
    sa.Column('nationality1', sa.String(100)),
    sa.Column('nationality2', sa.String(100), nullable=False),
    sa.Column('parent_team', sa.String(100)),
    sa.Column('fk_team_id',sa.Integer, nullable=False),
    sa.Column('fk_country_id', sa.Integer, nullable=False),
    )

    op.create_table(
    'player_metrics',
    sa.Column('metrics_id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('player_id', sa.Integer, nullable=False),
    sa.Column('playing_style', sa.String(100)),
    sa.Column('xTV', sa.Numeric),
    sa.Column('rating', sa.Numeric),
    sa.Column('potential', sa.Numeric),
    sa.Column('GBE_result', sa.String(100)),
    sa.Column('GBE_score', sa.Integer),
    sa.Column('base_value', sa.Numeric),
    sa.Column('estimated_salary', sa.Numeric),
    sa.Column('contract_expiry', sa.Date),
    )

    op.create_table(
    'player_history',
    sa.Column('player_history_id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('player_id', sa.Integer,nullable=False),
    sa.Column('name', sa.String(100), nullable=False),
    sa.Column('year', sa.Integer, nullable=False),
    sa.Column('month', sa.Integer, nullable=False),
    sa.Column('xTV', sa.Numeric, nullable=False),
    sa.Column('updatedAt', sa.DateTime),
    )

    op.create_table(
    'agencies',
    sa.Column('agency_id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('agency_name', sa.String),
    sa.Column('agency_verified', sa.Boolean),
    )


    op.create_table(
    'team',
    sa.Column('team_id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('team_name', sa.Integer),
    sa.Column('competition_id', sa.Integer),
    sa.Column('country_id', sa.Integer, nullable=False),
    )

   
    op.create_table(
    'team_history',
    sa.Column('team_history_id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('player_id', sa.Integer,),
    sa.Column('name', sa.String(100), nullable=False),
    sa.Column('from_team', sa.String(255), nullable=False),
    sa.Column('to_team', sa.String(255), nullable=False),
    sa.Column('start_date', sa.Date, nullable=False),
    sa.Column('end_date', sa.Date),
    sa.Column('transfer_type', sa.String(50), nullable=False),
    sa.Column('transfer_fee_euros', sa.Numeric(18, 2), nullable=False),
    sa.Column('created_at', sa.Date, nullable=False),
   
    )

    op.create_table(
        'player_agency',
        sa.Column('player_id', sa.Integer, primary_key=True),
        sa.Column('agency_id', sa.Integer, primary_key=True),

    )

   




def downgrade() -> None:
    op.drop_table('country')
    op.drop_table('competition')
    op.drop_table('players')
    op.drop_table('player_metrics')
    op.drop_table('player_history')
    op.drop_table('agencies')
    op.drop_table('team')
    op.drop_table('team_history')
    op.drop_table('player_agency')
