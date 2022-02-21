"""add content column to posts table

Revision ID: fbfdcb480075
Revises: 83f4019d3654
Create Date: 2022-02-21 18:29:20.106824

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbfdcb480075'
down_revision = '83f4019d3654'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
