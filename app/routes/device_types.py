from flask import Blueprint, render_template, current_app
from app.db import db
from app.models import HwFirmware
from sqlalchemy import func
import re

device_types_bp = Blueprint('device_types', __name__)

pattern = re.compile(r"^(?P<device_name>.+)-(?P<version>[^-]+)-(?P<revision>[^-]+)-g(?P<git_hash>[a-fA-F0-9]+)\.(bit|bin|mcs)$")

def get_device_types():
    """
    Fetch distinct device types (device_name) from base_name in hw_firmware.
    """
    base_names = db.session.query(HwFirmware.base_name).distinct()
    device_names = {pattern.match(bn.base_name).group("device_name") for bn in base_names if pattern.match(bn.base_name)}
    return sorted(device_names)

@device_types_bp.route("/")
def list_device_types():
    """
    List distinct device types.
    """
    current_app.logger.debug("Rendering device types list")
    device_types = get_device_types()
    indexed_device_types = [(idx + 1, name) for idx, name in enumerate(device_types)]
    return render_template("device_types.html", indexed_device_types=indexed_device_types)

@device_types_bp.route("/<device_type>")
def devices_by_type(device_type):
    """
    List all devices that belong to a specific device type.
    """
    current_app.logger.debug(f"Rendering devices for device type: {device_type}")

    devices = (db.session.query(HwFirmware)
               .filter(HwFirmware.base_name.like(f"{device_type}-%"))
               .order_by(HwFirmware.datetime.desc())
               .all())

    device_list = [
        {
            "index": idx + 1,
            "serial_number": fw.serialHex,
            "serial_link": f"/devices/{fw.serialHex}",
            "datetime": fw.datetime.isoformat(),
            "firmware": fw.base_name,
            "firmware_link": f"/firmwares/{fw.base_name}",
        }
        for idx, fw in enumerate(devices)
    ]

    return render_template("devices_by_type.html", device_type=device_type, device_list=device_list)
