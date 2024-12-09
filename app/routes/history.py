from flask import Blueprint, render_template, current_app
from app.db import db
from app.models import HwFirmware

history_bp = Blueprint('history', __name__)

@history_bp.route("/")
def firmware_history():
    """
    Display the last 1000 loaded firmware records, sorted by datetime descending.
    """
    current_app.logger.debug("Rendering firmware history page")

    # Query the last 1000 loaded firmware records
    firmware_records = (db.session.query(HwFirmware)
                        .order_by(HwFirmware.datetime.desc())
                        .limit(1000)
                        .all())

    # Preprocess data for rendering
    history = [
        {
            "datetime": fw.datetime.isoformat(),
            "serial_number": fw.serialHex,
            "serial_link": f"/devices/{fw.serialHex}",
            "firmware": fw.base_name,
            "firmware_link": f"/firmwares/{fw.base_name}",
        }
        for fw in firmware_records
    ]

    return render_template("history.html", history=history)
