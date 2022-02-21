"""add user table

Revision ID: aaa9946769fc
Revises: fbfdcb480075
Create Date: 2022-02-21 18:32:44.815966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aaa9946769fc'
down_revision = 'fbfdcb480075'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),  #we can define primary key in anyway
                    sa.UniqueConstraint('email')) #we can define unique constraint in anyway
    pass


def downgrade():
    op.drop_table('users')
    pass
