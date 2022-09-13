"""Development Database"""

# Standard library imports
# --- None ---

# Third party imports
from app import app

# Local application imports
# --- None ---


db_dialect='postgresql'
db_driver='psycopg2'
db_user='pythonapp'
db_pass=''
db_host='localhost'
db_port='5432'
db_name='dev_db'


# db = SQLAlchemy()
DATABASE_URI = f'{db_dialect}+{db_driver}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
# db.init_app(app)