"""Include timestamps

Revision ID: fb58a1cc7bfc
Revises: a7f4604fe27c
Create Date: 2022-09-04 14:07:47.904708

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import insert


# revision identifiers, used by Alembic.
revision = 'fb58a1cc7bfc'
down_revision = 'a7f4604fe27c'
branch_labels = None
depends_on = None


def upgrade():

    app_schema = 'flaskapp'

    # Create users table
    users = sa.table('users', 
        sa.Column('id', sa.Integer),#, autoincrement=True),
        sa.Column('username', sa.String(64)),
        sa.Column('email', sa.String(80)),
        sa.Column('created', sa.DateTime),
        sa.Column('admin', sa.Boolean),
        schema=app_schema
    )
    groups = sa.table('groups', 
        sa.Column('group', sa.String),
        sa.Column('owner', sa.Integer),
        schema=app_schema
    )

    # Find or Create 'System' user if not exists
    # NOTE: be cautious with data migrations inside DDL migrations
    conn = op.get_bind()
    sys_id = conn.execute(users.select().where(users.c.username=='System')).scalar()
    if not sys_id:
        sys_id = conn.execute(
            insert(users)
            .returning(users.c.id)
            .values(
                username='System',
                email='System@localhost',
                created=datetime.now(timezone.utc),
                admin=True
            )
            .on_conflict_do_nothing()
        ).scalar()

    # Add sys_id to current group.owner records (populate NULLs before 
    #   making the column NOT NULL)
    op.execute(
        groups
            .update()
            .where(groups.c.owner == None)
            .values(owner=sys_id)
    )

    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('groups', sa.Column('updated', sa.DateTime(), nullable=True), schema=app_schema)

    op.alter_column(
        'groups', 'owner',
        type_=sa.Integer,
        existing_type=sa.VARCHAR,
        nullable=False,
        existing_nullable=True,
        schema=app_schema,
        postgresql_using='owner::integer' # <-- important for PostgreSQL to convert existing data
    )

    # ALTER TABLE flaskapp.groups ALTER COLUMN owner TYPE INTEGER USING owner::integer;
    # ALTER TABLE flaskapp.groups ADD FOREIGN KEY (owner) REFERENCES users (id);
    op.create_foreign_key(None, 'groups', 'users', ['owner'], ['id'], source_schema=app_schema, referent_schema=app_schema)
    op.add_column('users', sa.Column('updated', sa.DateTime(), nullable=True), schema=app_schema)
    op.add_column('users_groups', sa.Column('created', sa.DateTime(), nullable=False), schema=app_schema)
    op.add_column('users_groups', sa.Column('updated', sa.DateTime(), nullable=True), schema=app_schema)
    # ### end Alembic commands ###


def downgrade():
    app_schema = 'flaskapp'

    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users_groups', 'updated', schema=app_schema)
    op.drop_column('users_groups', 'created', schema=app_schema)
    op.drop_column('users', 'updated', schema=app_schema)
    op.drop_constraint('groups_owner_fkey', 'groups', schema=app_schema, type_='foreignkey')
    op.alter_column('groups', 'owner',
        existing_type=sa.Integer,
        type_=sa.VARCHAR(length=64),
        nullable=True,
        schema=app_schema
    )
    op.drop_column('groups', 'updated', schema=app_schema)
    # ### end Alembic commands ###

    groups = sa.table('groups',
        sa.Column('group', sa.String),
        sa.Column('owner', sa.String),
        schema=app_schema
    )
    op.execute(
        groups
            .update()
            .values(owner=None)
    )
