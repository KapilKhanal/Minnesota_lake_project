from flask import Flask
import sys
import os

sys.path.append((os.path.dirname(os.path.dirname(__file__))))
print(sys.path)
from api.config import *


_logger = get_logger(logger_name=__name__)


def create_app(*, config_object) -> Flask:
    """Create a flask app instance."""

    flask_app = Flask('ml_api')
    flask_app.config.from_object(config_object)

    # import blueprints
    from api.controller import prediction_app
    flask_app.register_blueprint(prediction_app)
    _logger.debug('Application instance created')

    return flask_app
