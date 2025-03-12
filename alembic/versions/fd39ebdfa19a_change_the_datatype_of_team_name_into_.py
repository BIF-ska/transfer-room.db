"""change the datatype of team_name into string instead of int 

Revision ID: fd39ebdfa19a
Revises: b8afc4fb8723
Create Date: 2025-03-11 09:25:08.853969

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd39ebdfa19a'
down_revision: Union[str, None] = 'b8afc4fb8723'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('team', 'team_name',
                    type_=sa.String(),
                    existing_type=sa.Integer(),
                    nullable=False)  

def downgrade() -> None:
   
    op.alter_column('team', 'team_name',
                    type_=sa.Integer(),
                    existing_type=sa.String(),
                    nullable=False) 
