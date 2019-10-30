"""empty message

Revision ID: c5419613babf
Revises: 
Create Date: 2019-10-30 12:30:04.569736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5419613babf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('bio', sa.String(length=500), nullable=True))
    op.add_column('user', sa.Column('department', sa.String(length=64), nullable=True))
    op.add_column('user', sa.Column('fname', sa.String(length=64), nullable=True))
    op.add_column('user', sa.Column('lname', sa.String(length=64), nullable=True))
    op.add_column('user', sa.Column('major', sa.String(length=64), nullable=True))
    op.add_column('user', sa.Column('minor', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'minor')
    op.drop_column('user', 'major')
    op.drop_column('user', 'lname')
    op.drop_column('user', 'fname')
    op.drop_column('user', 'department')
    op.drop_column('user', 'bio')
    # ### end Alembic commands ###
