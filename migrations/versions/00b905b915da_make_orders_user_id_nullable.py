"""make orders.user_id nullable

Revision ID: 00b905b915da
Revises: 6b4f38045ca0
Create Date: 2024-11-08 03:33:15.713802

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00b905b915da'
down_revision = '6b4f38045ca0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_items', schema=None) as batch_op:
        batch_op.alter_column('order_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_items', schema=None) as batch_op:
        batch_op.alter_column('order_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
