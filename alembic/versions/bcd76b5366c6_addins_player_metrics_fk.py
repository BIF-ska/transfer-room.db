"""Addins player metrics fk 

Revision ID: bcd76b5366c6
Revises: cce2928c79cc
Create Date: 2025-02-12 11:38:09.470029

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bcd76b5366c6'
down_revision: Union[str, None] = 'cce2928c79cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    pass  # Tilføj migrationskode her



def downgrade():
    pass  # Tilføj rollback-kode her, hvis nødvendigt



