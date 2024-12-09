import os
from dotenv import load_dotenv
import pytz

def load_config(app):
    load_dotenv()  # Loads environment variables from .env

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', 3306)}/{os.getenv('DB_NAME')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Set logging level
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    app.logger.setLevel(log_level)

    app.config["TIMEZONE"] = pytz.timezone(os.getenv("TIMEZONE", "UTC"))
