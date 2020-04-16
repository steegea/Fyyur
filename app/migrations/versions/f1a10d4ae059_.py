"""empty message

Revision ID: f1a10d4ae059
Revises: 290c95052707
Create Date: 2020-04-01 14:54:21.470096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1a10d4ae059'
down_revision = '290c95052707'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('shows', 'artist_name')
    op.drop_column('shows', 'venue_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('venue_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('shows', sa.Column('artist_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
