"""Add TransferInfo and PlayersInfo tables

Revision ID: d8559da4b381
Revises: cded781e71ef
Create Date: 2025-02-14 11:39:14.252520

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8559da4b381'
down_revision: Union[str, None] = 'cded781e71ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Opret TransferInfo-tabellen
    op.create_table(
        'TransferInfo',
        sa.Column('TransferID', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('TransferValue', sa.Numeric(10, 2)),
        sa.Column('PlayerID', sa.Integer, sa.ForeignKey('Players.PlayerID', ondelete="CASCADE"), unique=True)
    )

    # Opret PlayersInfo-tabellen
    op.create_table(
    "PlayersInfo",
    sa.Column("PlayersInfoID", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("TransferID", sa.Integer, sa.ForeignKey("TransferInfo.TransferID", ondelete="CASCADE")),
    sa.Column("PlayerID", sa.Integer, sa.ForeignKey("Players.PlayerID", ondelete="NO ACTION")),  # Fjern CASCADE her
    sa.Column("Rating", sa.Numeric(3, 1))
)


def downgrade():
    # Slet tabellerne i omvendt rækkefølge for at undgå FK-konflikter
    op.drop_table('PlayersInfo')
    op.drop_table('TransferInfo')