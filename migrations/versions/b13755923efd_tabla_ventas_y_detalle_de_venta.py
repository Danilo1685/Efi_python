"""Tabla ventas y detalle de venta

Revision ID: b13755923efd
Revises: 44b0038d22bc
Create Date: 2024-08-11 23:44:39.732284

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b13755923efd'
down_revision = '44b0038d22bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('venta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cliente_id', sa.Integer(), nullable=False),
    sa.Column('fecha', sa.DateTime(), nullable=False),
    sa.Column('total', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cliente_id'], ['cliente.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('detalle_venta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('venta_id', sa.Integer(), nullable=False),
    sa.Column('telefono_id', sa.Integer(), nullable=False),
    sa.Column('cantidad', sa.Integer(), nullable=False),
    sa.Column('precio_unitario', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['telefono_id'], ['telefono.id'], ),
    sa.ForeignKeyConstraint(['venta_id'], ['venta.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('detalle_venta')
    op.drop_table('venta')
    # ### end Alembic commands ###
