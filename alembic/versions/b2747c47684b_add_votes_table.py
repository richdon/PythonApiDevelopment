"""add votes table

Revision ID: b2747c47684b
Revises: 98a2bc3c5bec
Create Date: 2022-06-22 20:13:57.596226

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2747c47684b'
down_revision = '98a2bc3c5bec'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('votes',
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('post_id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('user_id', 'post_id')
                    )


def downgrade():
    op.create_table('votes')
