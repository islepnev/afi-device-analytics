import sys
import csv
import logging

import sys
import csv
import logging

def load_device_registry(filepath=None):
    """
    Load Device Registry data from a CSV file or stdin.

    Args:
        filepath (str): Path to the CSV file. If None, read from stdin.

    Returns:
        Dict[str, Dict]: Dictionary of device records keyed by serial_number.
    """
    registry = {}
    seen = set()
    f = open(filepath, 'r') if filepath else sys.stdin
    reader = csv.DictReader(f)

    # Normalize headers
    reader.fieldnames = [h.strip().lower().replace(' ', '_') for h in reader.fieldnames]

    for row in reader:
        # Handle serial number field
        if 'serial_number' not in row and 'serialhex' in row:
            row['serial_number'] = row['serialhex']
            del row['serialhex']

        serial = row.get('serial_number', '').strip().upper()
        if not serial:
            # logging.warning("Skipping entry with undefined serial number.")
            continue

        if serial in seen:
            logging.warning(f"Duplicate serial number in Device Registry: {serial}. Ignoring subsequent entry.")
            continue

        seen.add(serial)
        row['serial_number'] = serial
        registry[serial] = row

    if f is not sys.stdin:
        f.close()
    return registry
