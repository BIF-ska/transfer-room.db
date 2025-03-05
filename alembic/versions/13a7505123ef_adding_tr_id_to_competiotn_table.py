"""adding Tr_id to Competiotn table  

Revision ID: 13a7505123ef
Revises: 0ae36a2ae109
Create Date: 2025-03-04 10:26:04.960682

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '13a7505123ef'
down_revision: Union[str, None] = '0ae36a2ae109'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
def upgrade():
   
    op.add_column("PlayerMetrics", sa.Column("GBEScore", sa.Integer, nullable=True))
    op.add_column("PlayerMetrics", sa.Column("BaseValue", sa.Numeric, nullable=True))
    op.add_column("PlayerMetrics", sa.Column("EstimatedSalary", sa.String, nullable=True))
    

    

def downgrade():
    op.drop_column("PlayerMetrics", "GBEScore")
    op.drop_column("PlayerMetrics", "BaseValue")
    op.drop_column("PlayerMetrics", "EstimatedSalary")
