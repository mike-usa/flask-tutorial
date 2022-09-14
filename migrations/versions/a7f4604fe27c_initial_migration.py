"""Initial migration

Revision ID: a7f4604fe27c
Revises: 
Create Date: 2022-09-03 18:07:40.638769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7f4604fe27c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    app_schema = 'flaskapp'

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('groups',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group', sa.String(length=64), nullable=False),
    sa.Column('owner', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('is_security', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema=app_schema
    )
    op.create_index(op.f(f'ix_{app_schema}_groups_group'), 'groups', ['group'], unique=True, schema=app_schema)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema=app_schema
    )
    op.create_index(op.f(f'ix_{app_schema}_users_email'), 'users', ['email'], unique=True, schema=app_schema)
    op.create_index(op.f(f'ix_{app_schema}_users_username'), 'users', ['username'], unique=True, schema=app_schema)
    op.create_table('users_groups',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], [f'{app_schema}.groups.id'], ),
    sa.ForeignKeyConstraint(['user_id'], [f'{app_schema}.users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'group_id'),
    schema=app_schema
    )
    # ### end Alembic commands ###


def downgrade():
    app_schema = 'flaskapp'

    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_groups', schema=app_schema)
    op.drop_index(op.f(f'ix_{app_schema}_users_username'), table_name='users', schema=app_schema)
    op.drop_index(op.f(f'ix_{app_schema}_users_email'), table_name='users', schema=app_schema)
    op.drop_table('users', schema=app_schema)
    op.drop_index(op.f(f'ix_{app_schema}_groups_group'), table_name='groups', schema=app_schema)
    op.drop_table('groups', schema=app_schema)
    # ### end Alembic commands ###