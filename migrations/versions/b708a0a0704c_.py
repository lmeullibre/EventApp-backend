"""empty message

Revision ID: b708a0a0704c
Revises: d0104171bdc1
Create Date: 2020-01-03 14:02:50.301628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b708a0a0704c'
down_revision = 'd0104171bdc1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Funded',
                    sa.Column('event_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('fund_amount', sa.Float(), nullable=True),
                    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('event_id', 'user_id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Funded')
    # ### end Alembic commands ###