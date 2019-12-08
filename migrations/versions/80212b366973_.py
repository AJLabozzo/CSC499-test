"""empty message

Revision ID: 80212b366973
Revises: 
Create Date: 2019-11-29 23:25:38.441799

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80212b366973'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clubs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_clubs_name'), 'clubs', ['name'], unique=True)
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('date', sa.String(length=120), nullable=True),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.Column('location', sa.String(length=128), nullable=True),
    sa.Column('organizer', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_events_name'), 'events', ['name'], unique=True)
    op.create_table('internships',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_internships_name'), 'internships', ['name'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('user_role', sa.String(length=64), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.Column('fname', sa.String(length=64), nullable=True),
    sa.Column('lname', sa.String(length=64), nullable=True),
    sa.Column('major', sa.String(length=64), nullable=True),
    sa.Column('minor', sa.String(length=64), nullable=True),
    sa.Column('bio', sa.String(length=500), nullable=True),
    sa.Column('department', sa.String(length=64), nullable=True),
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
    sa.Column('department', sa.String(length=64), nullable=True),
    sa.Column('progress', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_project_projectname'), 'project', ['projectname'], unique=True)
    op.create_index(op.f('ix_project_timestamp'), 'project', ['timestamp'], unique=False)
    op.create_table('goals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('g1', sa.Boolean(), nullable=True),
    sa.Column('g2', sa.Boolean(), nullable=True),
    sa.Column('g3', sa.Boolean(), nullable=True),
    sa.Column('g4', sa.Boolean(), nullable=True),
    sa.Column('g5', sa.Boolean(), nullable=True),
    sa.Column('g6', sa.Boolean(), nullable=True),
    sa.Column('g7', sa.Boolean(), nullable=True),
    sa.Column('g8', sa.Boolean(), nullable=True),
    sa.Column('g9', sa.Boolean(), nullable=True),
    sa.Column('g10', sa.Boolean(), nullable=True),
    sa.Column('g11', sa.Boolean(), nullable=True),
    sa.Column('g12', sa.Boolean(), nullable=True),
    sa.Column('g13', sa.Boolean(), nullable=True),
    sa.Column('g14', sa.Boolean(), nullable=True),
    sa.Column('g15', sa.Boolean(), nullable=True),
    sa.Column('g16', sa.Boolean(), nullable=True),
    sa.Column('g17', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_goals_project_id'), 'goals', ['project_id'], unique=True)
    op.create_table('members',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('member', sa.String(length=64), nullable=True),
    sa.Column('project', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['member'], ['user.username'], ),
    sa.ForeignKeyConstraint(['project'], ['project.projectname'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('members')
    op.drop_index(op.f('ix_goals_project_id'), table_name='goals')
    op.drop_table('goals')
    op.drop_index(op.f('ix_project_timestamp'), table_name='project')
    op.drop_index(op.f('ix_project_projectname'), table_name='project')
    op.drop_table('project')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_internships_name'), table_name='internships')
    op.drop_table('internships')
    op.drop_index(op.f('ix_events_name'), table_name='events')
    op.drop_table('events')
    op.drop_index(op.f('ix_clubs_name'), table_name='clubs')
    op.drop_table('clubs')
    # ### end Alembic commands ###