from __future__ import with_statement

import logging
from logging.config import fileConfig

from flask import current_app

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
config.set_main_option(
    'sqlalchemy.url',
    str(current_app.extensions['migrate'].db.get_engine().url).replace(
        '%', '%%'))
target_metadata = current_app.extensions['migrate'].db.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()

# import re
def include_name(name, type, parent_names):
    if type == 'schema':
        # if name == None:
        #     return False
        excludes = name in ['logs', 'test', 'tmp']
        # excludes = excludes or bool(re.search('^m\d', name)) # m1 and m3 accounts
        includes = name in ['public', 'flaskapp']
        # return name != 'flaskapp'
        return includes and not excludes

    return True


# def include_object(object, name, type_, reflected, compare_to):
#     print(f'include_object: {type_}')
#     print(f'include_object: {name}')
#     if type_ == "table":
#         print(f'include_object: [schema]{object.schema}')
#         print(f'include_object: [name]{object.name}')
#         print(f'include_object: [reflected]{reflected}')
#         print(f'include_object: [object]{object}')
#         print(f'include_object: [compare_to]{compare_to}')
#         if object.schema == None:
#             return False

#         excludes = object.schema in ['test', 'logs']
#         excludes = excludes or bool(
#             re.search('^m\d', object.schema))  # m1 and m3 accounts
#         includes = object.schema in ['public', 'flaskapp', 'api']

#         return object.schema != 'flaskapp'        
#         return includes and not excludes

#     return True
#         # if (type_ == "column" and
#         #     not reflected and
#         #         object.info.get("skip_autogenerate", False)):
#         #     return False
#         # else:
#         #     return True



def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # this callback is used to prevent an auto-migration from being generated
    # when there are no changes to the schema
    # reference: http://alembic.zzzcomputing.com/en/latest/cookbook.html
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    connectable = current_app.extensions['migrate'].db.get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
            **current_app.extensions['migrate'].configure_args,
            version_table='migrations',
            version_table_schema='flaskapp',
            include_schemas=True,
            include_name=include_name,
            compare_type=True
            # include_object=include_object
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()