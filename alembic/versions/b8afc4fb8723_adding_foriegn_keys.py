"""adding foriegn keys 

Revision ID: b8afc4fb8723
Revises: 76241bd6a6f8
Create Date: 2025-03-06 11:46:26.047412

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8afc4fb8723'
down_revision: Union[str, None] = '76241bd6a6f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key(
        'fk_players_country_id',
        'players',
        'country',
        ['fk_country_id'],
        ['country_id']
    )

    op.create_foreign_key(
        'fk_players_team_id',
        'players',
        'team',
        ['fk_team_id'],
        ['team_id']
    )
    
    op.create_foreign_key(
        'fk_players_competition_id',
        'players',
        'competition',
        ['competition_id'],
        ['competition_id']
    )

    op.create_foreign_key(
        'fk_team_country_id',
        'team',
        'country',
        ['country_id'],
        ['country_id']
    )

    op.create_foreign_key(
        'fk_team_competition_id',
        'team',
        'competition',
        ['competition_id'],
        ['competition_id']
    )

    op.create_foreign_key(
        'fk_competition_country_id',
        'competition',
        'country',
        ['country_id'],
        ['country_id']
    )

    op.create_foreign_key(
        'fk_player_metrics_player_id',
        'player_metrics',
        'players',
        ['player_id'],
        ['player_id']
    )
    
    op.create_foreign_key(
        'fk_player_history_player_id',
        'player_history',
        'players',
        ['player_id'],
        ['player_id']
    )
    
    op.create_foreign_key(
        'fk_player_agency_player_id',
        'player_agency',
        'players',
        ['player_id'],
        ['player_id']
    )

    op.create_foreign_key(
        'fk_player_agency_agency_id',
        'player_agency',
        'agencies',
        ['agency_id'],
        ['agency_id']
    )

    op.create_foreign_key(
        'fk_team_history_player_id',
        'team_history',
        'players',
        ['player_id'],
        ['player_id']
    )


def downgrade() -> None:
    op.drop_constraint('fk_team_history_player_id', 'team_history', type_='foreignkey')
    op.drop_constraint('fk_player_agency_agency_id', 'player_agency', type_='foreignkey')
    op.drop_constraint('fk_player_agency_player_id', 'player_agency', type_='foreignkey')
    op.drop_constraint('fk_player_history_player_id', 'player_history', type_='foreignkey')
    op.drop_constraint('fk_player_metrics_player_id', 'player_metrics', type_='foreignkey')

    op.drop_constraint('fk_competition_country_id', 'competition', type_='foreignkey')
    op.drop_constraint('fk_team_competition_id', 'team', type_='foreignkey')
    op.drop_constraint('fk_team_country_id', 'team', type_='foreignkey')

    op.drop_constraint('fk_players_competition_id', 'players', type_='foreignkey')
    op.drop_constraint('fk_players_team_id', 'players', type_='foreignkey')
    op.drop_constraint('fk_players_country_id', 'players', type_='foreignkey')