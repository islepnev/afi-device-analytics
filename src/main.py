import argparse
import logging

from .arg_parser import parse_args
from .summary import output_summary
from .logging_setup import setup_logging
from .db import get_session_factory
from .firmware_repo import get_latest_firmware_entries
from .device_registry import load_device_registry
from .processing import process_firmware_data, join_data
from .output import output_joined_data

def main():
    # Parse command-line arguments
    args = parse_args()

    setup_logging()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    Session = get_session_factory()
    session = Session()

    try:
        # Load device registry and firmware data
        device_data = load_device_registry(args.input_csv)
        fw_records = get_latest_firmware_entries(session)
        fw_data = process_firmware_data(fw_records)

        # Join and output data
        joined = join_data(fw_data, device_data)
        output_joined_data(joined, args.output_csv)

        # Print summaries to stdout
        output_summary(joined, args.summary)

    finally:
        session.close()

if __name__ == "__main__":
    main()
