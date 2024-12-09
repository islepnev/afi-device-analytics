from flask import Flask

from .config import load_config
from .db import init_db
from .routes.device_types import device_types_bp
from .routes.devices import devices_bp
from .routes.firmwares import firmwares_bp
from .routes.history import history_bp
from .routes.main import main_bp
from .routes.summaries import summaries_bp
from .utils import format_datetime

def create_app():
    app = Flask(__name__)
    load_config(app)
    init_db(app)

    # Register custom Jinja2 filter
    app.jinja_env.filters["format_datetime"] = format_datetime

    # Register Blueprints
    app.register_blueprint(main_bp, url_prefix="/")
    app.register_blueprint(summaries_bp, url_prefix="/summaries")
    app.register_blueprint(devices_bp, url_prefix="/devices")
    app.register_blueprint(firmwares_bp, url_prefix="/firmwares")
    app.register_blueprint(history_bp, url_prefix="/history")
    app.register_blueprint(device_types_bp, url_prefix="/device-types")

    return app
