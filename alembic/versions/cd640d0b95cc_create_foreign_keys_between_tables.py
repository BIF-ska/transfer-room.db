"""Create foreign keys between tables

Revision ID: cd640d0b95cc
Revises: f7efd8452dc6
Create Date: 2025-02-05 09:24:58.097495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd640d0b95cc'
down_revision: Union[str, None] = 'f7efd8452dc6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Tilføj foreign key constraints til eksisterende tabeller
    
    # Foreign key for Players table referencing Teams table
    op.create_foreign_key("fk_players_team", "Players", "Teams", ["PlayerID"], ["Team_id"])
    
    # Foreign key for Players table referencing Competition table
    op.create_foreign_key("fk_players_competition", "Players", "Competition", ["PlayerID"], ["Competition_id"])
    
    # Foreign key for PlayerMetrics table referencing Players table
    op.create_foreign_key("fk_playermetrics_player", "PlayerMetrics", "Players", ["PlayerID"], ["PlayerID"])
    
    # Foreign key for Playerhistory table referencing Teams table
    op.create_foreign_key("fk_playerhistory_team", "Playerhistory", "Teams", ["Player_id"], ["Team_id"])
    
    # Foreign key for TeamHistory table referencing Teams table
    op.create_foreign_key("fk_teamhistory_team", "TeamHistory", "Teams", ["TeamHistory_ID"], ["Team_id"])  

    
    # Foreign key for CoachMetrics table referencing HeadCoach table
    op.create_foreign_key("fk_coachmetrics_coach", "CoachMetrics", "HeadCoach", ["MetricID"], ["CoachID"])

def downgrade() -> None:
    # Drop the foreign key constraints on downgrade
    op.drop_constraint("fk_players_team", "Players", type_="foreignkey")
    op.drop_constraint("fk_players_competition", "Players", type_="foreignkey")
    op.drop_constraint("fk_playermetrics_player", "PlayerMetrics", type_="foreignkey")
    op.drop_constraint("fk_playerhistory_team", "Playerhistory", type_="foreignkey")
    op.drop_constraint("fk_teamhistory_team", "TeamHistory", type_="foreignkey")
    op.drop_constraint("fk_coachmetrics_coach", "CoachMetrics", type_="foreignkey")
