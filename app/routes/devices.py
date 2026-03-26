from flask import Blueprint, render_template, current_app
from app.db import db
from app.models import HwFirmware
from sqlalchemy import func
import re

devices_bp = Blueprint('devices', __name__)

pattern = re.compile(r"^(?P<firmware_type>.+)-(?P<version>[^-]+)-(?P<revision>[^-]+)-g(?P<git_hash>[a-fA-F0-9]+)\.(bit|bin|mcs)$")

def get_current_firmware_for_all_devices():
    subq = (db.session.query(
                HwFirmware.serialHex,
                func.max(HwFirmware.datetime).label("latest_dt")
            )
            .group_by(HwFirmware.serialHex)
            .subquery())

    latest_records = (db.session.query(HwFirmware)
                      .join(subq, (HwFirmware.serialHex == subq.c.serialHex) & (HwFirmware.datetime == subq.c.latest_dt))
                      .all())

    results = []
    for fw in latest_records:
        match = pattern.match(fw.base_name)
        if match:
            firmware_type = match.group("firmware_type")
            version = match.group("version")
        else:
            firmware_type = "Unknown"
            version = "Unknown"

        results.append({
            "serial_number": fw.serialHex.upper(),
            "firmware_type": firmware_type,
            "version": version
        })
    return results

@devices_bp.route("/")
def list_devices():
    current_app.logger.debug("Rendering devices list")
    devices_info = get_current_firmware_for_all_devices()
    # Sort by firmware_type
    devices_info = sorted(devices_info, key=lambda x: (x["firmware_type"], x["serial_number"]))
    return render_template("device_list.html", devices=devices_info)

@devices_bp.route("/<serial_number>")
def device_detail(serial_number):
    current_app.logger.debug(f"Rendering device detail for {serial_number}")
    # Get firmware history for this device
    fw_records = (db.session.query(HwFirmware)
                  .filter(func.upper(HwFirmware.serialHex) == serial_number.upper())
                  .order_by(HwFirmware.datetime.desc())
                  .all())

    history = []
    for fw in fw_records:
        match = pattern.match(fw.base_name)
        version = match.group("version") if match else "Unknown"
        history.append({
            "datetime": fw.datetime,
            "version": version,
            "firmware": fw.base_name,
            "firmware_link": f"/firmwares/{fw.base_name}",
            "goldImg": fw.goldImg,
            "path": fw.path,
            "fromHost": fw.fromHost
        })

    return render_template("device_detail.html", serial_number=serial_number.upper(), history=history)


def get_firmware_types():
    """
    Fetch distinct firmware types (firmware_type) from base_name in hw_firmware.
    """
    base_names = db.session.query(HwFirmware.base_name).distinct()
    firmware_types = {pattern.match(bn.base_name).group("firmware_type") for bn in base_names if pattern.match(bn.base_name)}
    return sorted(firmware_types)

@devices_bp.route("/firmware-types")
def list_firmware_types():
    """
    List distinct firmware types.
    """
    current_app.logger.debug("Rendering firmware types list")
    firmware_types = get_firmware_types()
    indexed_firmware_types = [(idx + 1, name) for idx, name in enumerate(firmware_types)]
    return render_template("firmware_types.html", indexed_firmware_types=indexed_firmware_types)
