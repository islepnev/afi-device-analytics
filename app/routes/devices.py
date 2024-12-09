from flask import Blueprint, render_template, current_app
from app.db import db
from app.models import HwFirmware
from sqlalchemy import func
import re

devices_bp = Blueprint('devices', __name__)

pattern = re.compile(r"^(?P<device_name>.+)-(?P<version>[^-]+)-(?P<revision>[^-]+)-g(?P<git_hash>[a-fA-F0-9]+)\.(bit|bin|mcs)$")

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
            device_name = match.group("device_name")
            version = match.group("version")
        else:
            device_name = "Unknown"
            version = "Unknown"

        results.append({
            "serial_number": fw.serialHex.upper(),
            "device_name": device_name,
            "version": version
        })
    return results

@devices_bp.route("/")
def list_devices():
    current_app.logger.debug("Rendering devices list")
    devices_info = get_current_firmware_for_all_devices()
    # Sort by device_name
    devices_info = sorted(devices_info, key=lambda x: (x["device_name"], x["serial_number"]))
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


def get_device_types():
    """
    Fetch distinct device types (device_name) from base_name in hw_firmware.
    """
    base_names = db.session.query(HwFirmware.base_name).distinct()
    device_names = {pattern.match(bn.base_name).group("device_name") for bn in base_names if pattern.match(bn.base_name)}
    return sorted(device_names)

@devices_bp.route("/device-types")
def list_device_types():
    """
    List distinct device types.
    """
    current_app.logger.debug("Rendering device types list")
    device_types = get_device_types()
    indexed_device_types = [(idx + 1, name) for idx, name in enumerate(device_types)]
    return render_template("device_types.html", indexed_device_types=indexed_device_types)
