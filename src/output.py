import sys
import csv
import logging
from typing import List, Dict


def output_joined_data(joined_records: List[Dict], output_path: str = None):
    """
    Write joined records to a CSV file or stdout.

    Args:
        joined_records (List[Dict]): List of joined records to output.
        output_path (str): File path to write output. Defaults to STDOUT.
    """
    if not joined_records:
        logging.info("No data to output.")
        return

    # Ensure fieldnames include all keys from all records
    fieldnames = sorted(set().union(*(rec.keys() for rec in joined_records)))

    # Log a warning if any record contains unexpected fields
    for rec in joined_records:
        extra_keys = set(rec.keys()) - set(fieldnames)
        if extra_keys:
            logging.warning(f"Record contains unexpected fields not in fieldnames: {extra_keys}")

    # Write the CSV output
    write_csv(joined_records, fieldnames, output_path)


def write_csv(joined_records: List[Dict], fieldnames: List[str], output_path: str = None):
    """
    Write joined records to a CSV file or stdout.

    Args:
        joined_records (List[Dict]): List of records to output.
        fieldnames (List[str]): List of CSV column headers.
        output_path (str): File path to write output. Defaults to STDOUT.
    """
    with open(output_path, 'w', newline='') if output_path else sys.stdout as out_f:
        writer = csv.DictWriter(out_f, fieldnames=fieldnames)
        writer.writeheader()
        for rec in joined_records:
            try:
                writer.writerow({k: (v if v is not None else '') for k, v in rec.items()})
            except ValueError as e:
                logging.error(f"Failed to write record: {rec}")
                raise e
