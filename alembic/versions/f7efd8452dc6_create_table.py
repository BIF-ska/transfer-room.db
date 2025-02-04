"""create_tables

Revision ID: f7efd8452dc6
Revises: 
Create Date: 2025-02-03 13:22:23.621979
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f7efd8452dc6'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create 'Country' table
    op.create_table(
        'Country',
        sa.Column('Country_id', sa.Integer, primary_key=True),
        sa.Column('Name', sa.String),
    )
    
    
def downgrade():
    
    
    # Drop 'Country' table
    op.drop_table('Country')
