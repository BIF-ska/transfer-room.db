"""REMOVING 2 columns from player teamhistory  

Revision ID: e8ba4b748e73
Revises: a46ac5c4c198
Create Date: 2025-03-05 12:23:38.669788

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8ba4b748e73'
down_revision: Union[str, None] = 'a46ac5c4c198'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    with op.batch_alter_table("Team_History") as batch_op:
        batch_op.drop_column("from_team_id")
        batch_op.drop_column("to_team_id")
    

    

def downgrade() -> None:
    pass
