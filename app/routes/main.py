from flask import Blueprint, render_template, current_app
from app.db import db
from app.models import HwFirmware
from sqlalchemy import func
import re

main_bp = Blueprint('main', __name__)

# Regex to extract version info from base_name
pattern = re.compile(r"^(?P<device_name>.+)-(?P<version>[^-]+)-(?P<revision>[^-]+)-g(?P<git_hash>[a-fA-F0-9]+)\.(bit|bin|mcs)$")

def get_totals():
    """
    Calculate total counts:
    - Total devices (distinct serial numbers)
    - Total device_name (Device Types, derived from base_name)
    - Total Firmware Versions (distinct base_name for the latest firmware per device)
    Fetch the last 10 loaded firmware records.
    """
    # Total devices: distinct serialHex
    total_devices = db.session.query(func.count(func.distinct(HwFirmware.serialHex))).scalar()

    # Total device_name (Device Types): distinct device_name extracted from base_name
    base_names = db.session.query(HwFirmware.base_name).distinct()
    device_names = {pattern.match(bn.base_name).group("device_name") for bn in base_names if pattern.match(bn.base_name)}
    total_device_types = len(device_names)

    # Total Firmware Versions: count distinct base_name for the latest firmware per device
    subq = (
        db.session.query(
            HwFirmware.serialHex,
            func.max(HwFirmware.datetime).label("latest_dt")
        )
        .group_by(HwFirmware.serialHex)
        .subquery()
    )

    latest_firmwares = (
        db.session.query(HwFirmware.base_name)
        .join(subq, (HwFirmware.serialHex == subq.c.serialHex) & (HwFirmware.datetime == subq.c.latest_dt))
        .distinct()
    )

    total_versions = latest_firmwares.count()

    # Last 10 loaded firmwares
    last_10_firmwares = (db.session.query(HwFirmware)
                         .order_by(HwFirmware.datetime.desc())
                         .limit(10)
                         .all())

    latest_firmwares = [
        {
            "datetime": fw.datetime.isoformat(),
            "serial_number": fw.serialHex,
            "serial_link": f"/devices/{fw.serialHex}",
            "firmware": fw.base_name,
            "firmware_link": f"/firmwares/{fw.base_name}",
        }
        for fw in last_10_firmwares
    ]

    return {
        "total_devices": total_devices,
        "total_device_types": total_device_types,
        "total_versions": total_versions,
        "latest_firmwares": latest_firmwares,
    }

@main_bp.route("/")
def index():
    current_app.logger.debug("Rendering index page")
    totals = get_totals()
    return render_template("index.html", totals=totals, latest_firmwares=totals["latest_firmwares"])
