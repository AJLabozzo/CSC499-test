"""tables

Revision ID: bf0a400fc741
Revises: 
Create Date: 2019-09-29 21:30:03.130682

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf0a400fc741'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('goals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('goal', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_goals_goal'), 'goals', ['goal'], unique=True)
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roles_role'), 'roles', ['role'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('user_role', sa.Integer(), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_role'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('project',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('projectname', sa.String(length=64), nullable=True),
    sa.Column('body', sa.String(length=500), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_project_projectname'), 'project', ['projectname'], unique=True)
    op.create_index(op.f('ix_project_timestamp'), 'project', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_project_timestamp'), table_name='project')
    op.drop_index(op.f('ix_project_projectname'), table_name='project')
    op.drop_table('project')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_roles_role'), table_name='roles')
    op.drop_table('roles')
    op.drop_index(op.f('ix_goals_goal'), table_name='goals')
    op.drop_table('goals')
    # ### end Alembic commands ###
