import logging
import os


logger = logging.getLogger(__name__)


class Config:

    SERVICE_PORT = None
    SERVICE_DEBUG = None

    def __init__(self, app, db):
        """
        Initiates microservice configuration
        :param app: Flask application context object
        :param db: SqlAlchemy database object
        :return: configuration object
        """
        self.app = app
        self.db = db
        self._init_db(app)
        self._init_service_port()
        self._init_service_debug()

    def _init_service_port(self):
        self.SERVICE_PORT = os.getenv('SERVICE_PORT')
        if not self.SERVICE_PORT:
            self.SERVICE_PORT = 8888

    def _init_service_debug(self):
        env_var = os.getenv('SERVICE_DEBUG')
        self.SERVICE_DEBUG = False if env_var == 'False' else True

    def _init_db(self, app):
        DATABASE_NAME = os.getenv('DATABASE_NAME')
        if not DATABASE_NAME:
            DATABASE_NAME = 'legyakoribb'

        DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
        if not DATABASE_PASSWORD:
            DATABASE_PASSWORD = 'testp'

        DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
        if not DATABASE_USERNAME:
            DATABASE_USERNAME = 'testu'

        DATABASE_HOST = os.getenv('DATABASE_HOST')
        if not DATABASE_HOST:
            DATABASE_HOST = 'localhost'

        logger.info('Connection properties: DB: %s, User: %s, Host: %s' % (
            DATABASE_NAME, DATABASE_USERNAME, DATABASE_HOST))
        # Flask-SQLAlchemy should extract connection string from the
        # application config
        app.config['SQLALCHEMY_DATABASE_URI'] = build_connection_url(
            DATABASE_USERNAME,
            DATABASE_PASSWORD,
            DATABASE_HOST,
            5432,
            DATABASE_NAME)
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.db.init_app(app)


def build_connection_url(user, password, host, port, dbname):
    if os.getenv('MYSQL_DATABASE_CONNECTION'):
        return f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbname}'
    return f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}'
