"""One-to-many ownership

Revision ID: aca3c96f4a12
Revises: fb58a1cc7bfc
Create Date: 2022-09-05 22:30:30.160485

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aca3c96f4a12'
down_revision = 'fb58a1cc7bfc'
branch_labels = None
depends_on = None


def upgrade():
    app_schema='flaskapp'
    
    # First create nullable column, then populate the values, then make non-nullable
    op.add_column('groups', sa.Column('owner_id', sa.Integer()), schema=app_schema)
    op.create_foreign_key(None, 'groups', 'users', ['owner_id'], ['id'], source_schema=app_schema, referent_schema=app_schema)
    op.execute(f'UPDATE {app_schema}.groups SET owner_id = owner;')
    op.alter_column('groups', sa.Column('owner_id', nullable=False))
    
    op.drop_constraint('groups_owner_fkey', 'groups', schema=app_schema, type_='foreignkey')
    op.drop_column('groups', 'owner', schema=app_schema)


def downgrade():
    app_schema = 'flaskapp'

    op.add_column('groups', sa.Column('owner', sa.INTEGER(), autoincrement=False), schema=app_schema)
    op.create_foreign_key(None, 'groups', 'users', ['owner'], ['id'], source_schema=app_schema, referent_schema=app_schema)
    op.execute(f'UPDATE {app_schema}.groups SET owner = owner_id;')
    op.alter_column('groups', sa.Column('owner', nullable=False))

    op.drop_constraint('groups_owner_id_fkey', 'groups',
                       schema=app_schema, type_='foreignkey')
    op.drop_column('groups', 'owner_id', schema=app_schema)
