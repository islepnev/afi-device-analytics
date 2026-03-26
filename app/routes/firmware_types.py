from flask import Blueprint, render_template, current_app
from app.db import db
from app.models import HwFirmware
from sqlalchemy import func
import re

firmware_types_bp = Blueprint('firmware_types', __name__)

pattern = re.compile(r"^(?P<firmware_type>.+)-(?P<version>[^-]+)-(?P<revision>[^-]+)-g(?P<git_hash>[a-fA-F0-9]+)\.(bit|bin|mcs)$")

def get_firmware_types():
    """
    Fetch distinct firmware types (firmware_type) from base_name in hw_firmware.
    """
    base_names = db.session.query(HwFirmware.base_name).distinct()
    firmware_types = {pattern.match(bn.base_name).group("firmware_type") for bn in base_names if pattern.match(bn.base_name)}
    return sorted(firmware_types)

@firmware_types_bp.route("/")
def list_firmware_types():
    """
    List distinct firmware types.
    """
    current_app.logger.debug("Rendering firmware types list")
    firmware_types = get_firmware_types()
    indexed_firmware_types = [(idx + 1, name) for idx, name in enumerate(firmware_types)]
    return render_template("firmware_types.html", indexed_firmware_types=indexed_firmware_types)

@firmware_types_bp.route("/<firmware_type>")
def devices_by_type(firmware_type):
    """
    List all devices that belong to a specific firmware type.
    """
    current_app.logger.debug(f"Rendering devices for firmware type: {firmware_type}")

    devices = (db.session.query(HwFirmware)
               .filter(HwFirmware.base_name.like(f"{firmware_type}-%"))
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

    return render_template("devices_by_type.html", firmware_type=firmware_type, device_list=device_list)
