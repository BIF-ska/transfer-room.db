"""add fk columns to teams

Revision ID: 0cb2c2f29925
Revises: b8111a1c7faf
Create Date: 2025-02-10 11:02:29.719547

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0cb2c2f29925'
down_revision: Union[str, None] = 'b8111a1c7faf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Add foreign key constraints
    op.create_foreign_key(
        'fk_teams_country',   # Constraint name
        'teams',              # Table with the foreign key
        'country',            # Referenced table
        ['country_id'],       # Column in 'teams' table
        ['country_id']        # Referenced column in 'country' table
    )
    
    op.create_foreign_key(
        'fk_teams_competition', 
        'teams', 
        'competition', 
        ['competition_id'], 
        ['competition_id']
    )

def downgrade() -> None:
    # Remove foreign key constraints if downgrading
    op.drop_constraint('fk_teams_country', 'teams', type_='foreignkey')
    op.drop_constraint('fk_teams_competition', 'teams', type_='foreignkey')
