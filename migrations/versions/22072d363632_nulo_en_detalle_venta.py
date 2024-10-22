"""nulo en detalle_venta

Revision ID: 22072d363632
Revises: 6bc839450f35
Create Date: 2024-10-10 01:06:41.048950

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '22072d363632'
down_revision = '6bc839450f35'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('detalle_venta', schema=None) as batch_op:
        batch_op.alter_column('telefono_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('detalle_venta', schema=None) as batch_op:
        batch_op.alter_column('telefono_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)

    # ### end Alembic commands ###