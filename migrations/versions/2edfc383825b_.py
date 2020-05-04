"""06. Genre column updation to String Array 

Revision ID: 2edfc383825b
Revises: 06790d1ff81b
Create Date: 2020-05-02 17:32:07.736885

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2edfc383825b'
down_revision = '06790d1ff81b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('genres', sa.ARRAY(sa.String()), nullable=True))
    op.add_column('Venue', sa.Column('genres', sa.ARRAY(sa.String()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'genres')
    op.drop_column('Artist', 'genres')
    # ### end Alembic commands ###
