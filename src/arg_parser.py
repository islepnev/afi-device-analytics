import argparse

def parse_args():
    """
    Parse command-line arguments for the QA Data Analysis script.

    Returns:
        Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="QA Data Analysis Script")
    parser.add_argument("input_csv", nargs="?", default=None,
                        help="Path to the Device Registry CSV file (or read from STDIN).")
    parser.add_argument("output_csv", nargs="?", default=None,
                        help="Path to the output CSV file (or write to STDOUT).")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging.")
    parser.add_argument("--summary", nargs="?", const=None, 
                        help="Generate a summary and output to the specified file. "
                             "If no file is specified, output to stdout.")

    args = parser.parse_args()

    if args.summary and not args.output_csv:
        parser.error("--summary requires an output file name to avoid mixing with STDOUT output.")

    return args
