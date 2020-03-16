"""empty message

Revision ID: f63274ab6631
Revises: e4fcadb93e83
Create Date: 2019-12-11 19:08:21.823289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f63274ab6631'
down_revision = 'e4fcadb93e83'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('backers', sa.Column('backed_amount', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('backers', 'backed_amount')
    # ### end Alembic commands ###