"""empty message

Revision ID: 882d5303fcf3
Revises: e6749c7ef0eb
Create Date: 2020-01-07 23:41:47.975669

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '882d5303fcf3'
down_revision = 'e6749c7ef0eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('event', 'lat',
               existing_type=mysql.FLOAT(),
               type_=sa.Numeric(precision=11, scale=8),
               existing_nullable=True)
    op.alter_column('event', 'long',
               existing_type=mysql.FLOAT(),
               type_=sa.Numeric(precision=11, scale=8),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('user_id_UNIQUE', 'vote', ['user_id'], unique=True)
    op.create_index('event_id_UNIQUE', 'vote', ['event_id'], unique=True)
    op.alter_column('event', 'long',
               existing_type=sa.Numeric(precision=11, scale=8),
               type_=mysql.FLOAT(),
               existing_nullable=True)
    op.alter_column('event', 'lat',
               existing_type=sa.Numeric(precision=11, scale=8),
               type_=mysql.FLOAT(),
               existing_nullable=True)
    # ### end Alembic commands ###
