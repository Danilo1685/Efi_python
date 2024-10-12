"""nulo en detalle_venta

Revision ID: 84e819b734d8
Revises: 22072d363632
Create Date: 2024-10-10 01:13:26.727805

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '84e819b734d8'
down_revision = '22072d363632'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stock', schema=None) as batch_op:
        batch_op.alter_column('telefono_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stock', schema=None) as batch_op:
        batch_op.alter_column('telefono_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)

    # ### end Alembic commands ###
