"""empty message

Revision ID: d1576ada0b0c
Revises: 5a4499d0b275
Create Date: 2020-01-07 23:46:16.604175

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd1576ada0b0c'
down_revision = '5a4499d0b275'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('event', 'lat',
               existing_type=mysql.DECIMAL(precision=11, scale=6),
               type_=sa.Numeric(precision=11, scale=8),
               existing_nullable=True)
    op.alter_column('event', 'long',
               existing_type=mysql.DECIMAL(precision=11, scale=6),
               type_=sa.Numeric(precision=11, scale=8),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('user_id_UNIQUE', 'vote', ['user_id'], unique=True)
    op.create_index('event_id_UNIQUE', 'vote', ['event_id'], unique=True)
    op.alter_column('event', 'long',
               existing_type=sa.Numeric(precision=11, scale=8),
               type_=mysql.DECIMAL(precision=11, scale=6),
               existing_nullable=True)
    op.alter_column('event', 'lat',
               existing_type=sa.Numeric(precision=11, scale=8),
               type_=mysql.DECIMAL(precision=11, scale=6),
               existing_nullable=True)
    # ### end Alembic commands ###