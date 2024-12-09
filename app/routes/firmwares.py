from flask import Blueprint, render_template, current_app
from app.db import db
from app.models import HwFirmware
from sqlalchemy import func

firmwares_bp = Blueprint('firmwares', __name__)

@firmwares_bp.route("/")
def list_firmwares():
    """
    List all firmwares based on the latest firmware loaded per device.
    (Previously known as firmware_versions)
    """
    current_app.logger.debug("Rendering firmware list")

    # Subquery to get the latest firmware per device
    subq = (
        db.session.query(
            HwFirmware.serialHex,
            func.max(HwFirmware.datetime).label("latest_dt")
        )
        .group_by(HwFirmware.serialHex)
        .subquery()
    )

    # Latest firmware for each device
    latest_firmwares = (
        db.session.query(HwFirmware.base_name)
        .join(subq, (HwFirmware.serialHex == subq.c.serialHex) & (HwFirmware.datetime == subq.c.latest_dt))
        .all()
    )

    firmware_counts = {}
    for record in latest_firmwares:
        firmware_counts[record.base_name] = firmware_counts.get(record.base_name, 0) + 1

    firmware_list = [
        {"index": idx + 1, "base_name": base_name, "count": count}
        for idx, (base_name, count) in enumerate(sorted(firmware_counts.items()))
    ]

    return render_template("firmwares.html", firmware_list=firmware_list)

@firmwares_bp.route("/<firmware>")
def firmware_details(firmware):
    """
    List all devices that currently have the specified firmware loaded.
    """
    current_app.logger.debug(f"Rendering firmware details for: {firmware}")

    # Subquery to get the latest firmware per device
    subq = (
        db.session.query(
            HwFirmware.serialHex,
            func.max(HwFirmware.datetime).label("latest_dt")
        )
        .group_by(HwFirmware.serialHex)
        .subquery()
    )

    # Query to find devices with the specified firmware as their latest
    devices = (
        db.session.query(HwFirmware)
        .join(subq, (HwFirmware.serialHex == subq.c.serialHex) & (HwFirmware.datetime == subq.c.latest_dt))
        .filter(HwFirmware.base_name == firmware)
        .order_by(HwFirmware.serialHex.asc())
        .all()
    )

    device_list = [
        {
            "index": idx + 1,
            "serial_number": fw.serialHex,
            "serial_link": f"/devices/{fw.serialHex}",
            "datetime": fw.datetime.isoformat(),
            "goldImg": "Yes" if fw.goldImg else "No"
        }
        for idx, fw in enumerate(devices)
    ]

    return render_template("firmware_details.html", firmware=firmware, device_list=device_list)
