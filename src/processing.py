import logging

import logging

import re
import logging

def process_firmware_data(firmware_records, ignore_suffixes=None):
    """
    Process and normalize Firmware Data.

    Args:
        firmware_records (List[HwFirmware]): Firmware records from the database.
        ignore_suffixes (List[str]): List of suffixes to strip from device_name.

    Returns:
        List[Dict]: Processed firmware records as dictionaries.
    """
    if ignore_suffixes is None:
        ignore_suffixes = [".bit", ".bin", ".mcs"]

    # Regex pattern to parse base_name
    pattern = re.compile(r"^(?P<device_name>.+)-(?P<version>[^-]+)-(?P<revision>[^-]+)-g(?P<git_hash>[a-fA-F0-9]+)\.(bit|bin|mcs)$")

    processed = []

    for rec in firmware_records:
        record = {
            'datetime': rec.datetime.isoformat() if rec.datetime else None,
            'revision': rec.revision,
            'fw_maj': rec.fw_maj,
            'fw_min': rec.fw_min,
            'base_name': rec.base_name,
            'pcb_name': rec.pcb_name,
            'path': rec.path,
            'fromHost': rec.fromHost,
            'goldImg': 1 if rec.goldImg else 0,
            'serial_number': rec.serialHex.strip().upper() if rec.serialHex else None
        }

        base_name = record.get('base_name', '')

        # Parse base_name using regex
        match = pattern.match(base_name)
        if not match:
            # logging.warning(f"Ignoring record with invalid base_name: {record}")
            continue

        # Extract parsed fields
        device_name = match.group("device_name")
        version = match.group("version")
        revision = match.group("revision")
        git_hash = match.group("git_hash")

        # Strip suffix from device_name
        for suffix in ignore_suffixes:
            if device_name.endswith(suffix):
                device_name = device_name[: -len(suffix)]

        record['device_name'] = device_name
        record['version'] = version
        record['revision'] = revision
        record['git_hash'] = git_hash

        processed.append(record)

    return processed


def join_data(firmware_data, device_data):
    joined = []
    for f in firmware_data:
        serial = f['serial_number']
        dev_info = device_data.get(serial, {})
        row = {**f, **dev_info}
        joined.append(row)
    return joined
