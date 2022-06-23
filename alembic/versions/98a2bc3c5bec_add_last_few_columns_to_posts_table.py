"""add last few columns to posts table

Revision ID: 98a2bc3c5bec
Revises: 5f03ed4382df
Create Date: 2022-06-22 18:49:54.232310

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98a2bc3c5bec'
down_revision = '5f03ed4382df'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
