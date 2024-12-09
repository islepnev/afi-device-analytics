from flask import Blueprint, render_template, current_app
from app.db import db
from app.models import HwFirmware
from datetime import datetime
import re
from sqlalchemy import func

summaries_bp = Blueprint('summaries', __name__)

# Regex to extract version info from base_name
pattern = re.compile(r"^(?P<device_name>.+)-(?P<version>[^-]+)-(?P<revision>[^-]+)-g(?P<git_hash>[a-fA-F0-9]+)\.(bit|bin|mcs)$")

def get_current_firmware_per_device():
    """
    For each device (identified by serialHex), find the latest hw_firmware entry by datetime,
    extract version and device_name from base_name.
    Returns a list of dicts: {device_name, version}
    """
    # Subquery: for each serialHex, find max datetime
    subq = (db.session.query(
                HwFirmware.serialHex,
                func.max(HwFirmware.datetime).label("latest_dt")
            )
            .group_by(HwFirmware.serialHex)
            .subquery())

    # Join hw_firmware with subquery to get latest record per device
    latest_records = (db.session.query(HwFirmware)
                      .join(subq, (HwFirmware.serialHex == subq.c.serialHex) & (HwFirmware.datetime == subq.c.latest_dt))
                      .all())

    results = []
    for fw in latest_records:
        # Parse version and device_name from base_name
        match = pattern.match(fw.base_name)
        if match:
            device_name = match.group("device_name")
            version = match.group("version")
        else:
            device_name = "Unknown"
            version = "Unknown"

        results.append({"device_name": device_name, "version": version})
    return results

@summaries_bp.route("/")
def show_summaries():
    current_app.logger.debug("Rendering summaries page")
    current_data = get_current_firmware_per_device()

    # Count how many devices run each (device_name, version)
    combo_map = {}
    for row in current_data:
        key = (row["device_name"], row["version"])
        combo_map[key] = combo_map.get(key, 0) + 1

    summary_rows = []
    total_count = 0
    for (dev_name, ver), cnt in sorted(combo_map.items()):
        summary_rows.append({"device_name": dev_name, "version": ver, "count": cnt})
        total_count += cnt

    summary_rows.append({"device_name": "**Total**", "version": "", "count": total_count})

    return render_template("summaries.html", summary_rows=summary_rows)
