"""add content column

Revision ID: ef70fe9bb5cd
Revises: 67b90aed44fe
Create Date: 2022-05-30 22:47:37.648408

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef70fe9bb5cd'
down_revision = '67b90aed44fe'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
