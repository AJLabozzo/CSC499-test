"""empty message

Revision ID: 57fbc5f03b32
Revises: 9eced8f220b1
Create Date: 2019-11-18 20:53:28.130101

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57fbc5f03b32'
down_revision = '9eced8f220b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goals', sa.Column('g1', sa.Boolean(), nullable=True))
    op.add_column('goals', sa.Column('g10', sa.Boolean(), nullable=True))
    op.add_column('goals', sa.Column('g11', sa.Boolean(), nullable=True))
    op.add_column('goals', sa.Column('g12', sa.Boolean(), nullable=True))
    op.add_column('goals', sa.Column('g13', sa.Boolean(), nullable=True))
    op.add_column('goals', sa.Column('g14', sa.Boolean(), nullable=True))
    op.add_column('goals', sa.Column('g15', sa.Boolean(), nullable=True))
    op.add_column('goals', sa.Column('g16', sa.Boolean(), nullable=True))
    op.add_column('goals', sa.Column('g17', sa.Boolean(), nullable=True))
    op.add_column('goals', sa.Column('g2', sa.Boolean(), nullable=True))
    op.add_column('goals', sa.Column('g3', sa.Boolean(), nullable=True))
    op.add_column('goals', sa.Column('g4', sa.Boolean(), nullable=True))
    op.add_column('goals', sa.Column('g5', sa.Boolean(), nullable=True))
    op.add_column('goals', sa.Column('g6', sa.Boolean(), nullable=True))
    op.add_column('goals', sa.Column('g7', sa.Boolean(), nullable=True))
    op.add_column('goals', sa.Column('g8', sa.Boolean(), nullable=True))
    op.add_column('goals', sa.Column('g9', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('goals', 'g9')
    op.drop_column('goals', 'g8')
    op.drop_column('goals', 'g7')
    op.drop_column('goals', 'g6')
    op.drop_column('goals', 'g5')
    op.drop_column('goals', 'g4')
    op.drop_column('goals', 'g3')
    op.drop_column('goals', 'g2')
    op.drop_column('goals', 'g17')
    op.drop_column('goals', 'g16')
    op.drop_column('goals', 'g15')
    op.drop_column('goals', 'g14')
    op.drop_column('goals', 'g13')
    op.drop_column('goals', 'g12')
    op.drop_column('goals', 'g11')
    op.drop_column('goals', 'g10')
    op.drop_column('goals', 'g1')
    # ### end Alembic commands ###