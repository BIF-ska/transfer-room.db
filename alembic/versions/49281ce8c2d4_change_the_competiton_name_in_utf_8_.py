"""change the competiton name in UTF-8 Support 

Revision ID: 49281ce8c2d4
Revises: fd39ebdfa19a
Create Date: 2025-03-11 14:46:54.404067

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49281ce8c2d4'
down_revision: Union[str, None] = 'fd39ebdfa19a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Alter competition_name and team_name to NVARCHAR for Unicode support."""
    op.execute("""
        ALTER TABLE competition 
        ALTER COLUMN competition_name NVARCHAR(255) COLLATE Latin1_General_CI_AI;
    """)

    op.execute("""
        ALTER TABLE team
        ALTER COLUMN team_name NVARCHAR(255) COLLATE Latin1_General_CI_AI;
    """)

def downgrade() -> None:
    """Revert competition_name and team_name to original VARCHAR encoding."""
    op.execute("""
        ALTER TABLE competition 
        ALTER COLUMN competition_name VARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS;
    """)

    op.execute("""
        ALTER TABLE team
        ALTER COLUMN team_name VARCHAR(255) COLLATE SQL_Latin1_General_CP1_CI_AS;
    """)
