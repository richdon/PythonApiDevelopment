"""add user table

Revision ID: 61ed5351e665
Revises: ef70fe9bb5cd
Create Date: 2022-06-22 18:15:57.172309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61ed5351e665'
down_revision = 'ef70fe9bb5cd'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )


def downgrade():
    op.drop_table('users')
