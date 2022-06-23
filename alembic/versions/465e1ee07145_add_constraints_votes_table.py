"""add constraints votes table

Revision ID: 465e1ee07145
Revises: b2747c47684b
Create Date: 2022-06-22 20:15:03.547439

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '465e1ee07145'
down_revision = 'b2747c47684b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key('vote_users_fk', source_table='votes', referent_table='users',
                          local_cols=['user_id'], remote_cols=['id'], ondelete='CASCADE'),

    op.create_foreign_key('vote_posts_fk', source_table='votes', referent_table='posts',
                          local_cols=['post_id'], remote_cols=['id'], ondelete='CASCADE'),


def downgrade():
    op.drop_constraint('vote_users_fk', table_name='votes')
    op.drop_constraint('vote_posts_fk', table_name='votes')
