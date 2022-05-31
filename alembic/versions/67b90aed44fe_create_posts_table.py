"""create posts table

Revision ID: 67b90aed44fe
Revises: 
Create Date: 2022-05-30 22:32:25.839743

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '67b90aed44fe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                             sa.Column('title', sa.String(), nullable=False))


def downgrade():
    op.drop_table('posts')
