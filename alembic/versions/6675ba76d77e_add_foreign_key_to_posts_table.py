"""add foreign key to posts table

Revision ID: 6675ba76d77e
Revises: aaa9946769fc
Create Date: 2022-02-21 18:38:54.264039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6675ba76d77e'
down_revision = 'aaa9946769fc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users",
                            local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
