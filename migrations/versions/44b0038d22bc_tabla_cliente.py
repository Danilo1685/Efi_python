"""Tabla Cliente

Revision ID: 44b0038d22bc
Revises: 29619432cd5e
Create Date: 2024-08-11 22:47:53.022798

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44b0038d22bc'
down_revision = '29619432cd5e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cliente',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('correo', sa.String(length=100), nullable=False),
    sa.Column('telefono', sa.String(length=15), nullable=True),
    sa.Column('direccion', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('correo')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cliente')
    # ### end Alembic commands ###
