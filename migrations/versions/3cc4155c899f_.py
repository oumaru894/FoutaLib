"""empty message

Revision ID: 3cc4155c899f
Revises: ce194b707e36
Create Date: 2024-11-08 03:36:26.016107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3cc4155c899f'
down_revision = 'ce194b707e36'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.alter_column('payment_method',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.alter_column('payment_method',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)

    # ### end Alembic commands ###