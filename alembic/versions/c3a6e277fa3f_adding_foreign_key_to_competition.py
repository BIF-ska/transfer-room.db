"""adding foreign key to competition

Revision ID: c3a6e277fa3f
Revises: 2d5994d68578
Create Date: 2025-02-07 10:57:26.137441

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3a6e277fa3f'
down_revision: Union[str, None] = '2d5994d68578'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Opret en fremmednøgle fra 'Competition.Country_id' til 'Country.country_id'
    op.create_foreign_key(
        'fk_competition_country',  # Navnet på fremmednøglen
        'Competition',             # Hovedtabellen, der skal have fremmednøglen
        'Country',                 # Referencetabellen (den tabel, der indeholder den primære nøgle)
        ['Country_id'],            # Kolonnen i 'Competition' (hvor fremmednøglen skal være)
        ['country_id'],            # Kolonnen i 'Country', som er den primære nøgle
    )

def downgrade():
    # Fjern fremmednøglen, hvis du ønsker at rulle tilbage
    op.drop_constraint('fk_competition_country', 'Competition', type_='foreignkey')
