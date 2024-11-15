"""make orders.user_id nullable

Revision ID: ce194b707e36
Revises: 00b905b915da
Create Date: 2024-11-08 03:34:52.046009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce194b707e36'
down_revision = '00b905b915da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_items', schema=None) as batch_op:
        batch_op.alter_column('order_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    with op.batch_alter_table('order_items', schema=None) as batch_op:
        batch_op.alter_column('order_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
