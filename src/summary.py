from collections import defaultdict
from datetime import datetime
from tabulate import tabulate
from typing import List, Dict
import logging


from jinja2 import Environment, FileSystemLoader

def render_template(template_name: str, context: Dict) -> str:
    """
    Render a Jinja template with the given context.

    Args:
        template_name (str): Name of the template file.
        context (Dict): Context dictionary for rendering.

    Returns:
        str: Rendered template as a string.
    """
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(template_name)
    return template.render(context)


def generate_version_summary(joined_records: List[Dict]) -> List[Dict]:
    """
    Generate a version summary table showing how many devices run each (device_name, version).
    This is determined by selecting the latest record per serial_number (device) based on datetime.

    Args:
        joined_records (List[Dict]): List of joined records, each representing a firmware load event.

    Returns:
        List[Dict]: Summary table rows with keys: device_name, version, count.
    """

    # Step 1: Identify the latest record per device
    # Map: serial_number -> record with max datetime
    latest_per_device = {}
    for record in joined_records:
        serial = record.get('serial_number')
        if not serial:
            continue
        current_dt = record.get('datetime')
        if not current_dt:
            continue
        # Convert to datetime object if needed (assuming isoformat string)
        dt_obj = datetime.fromisoformat(current_dt)
        if serial not in latest_per_device or dt_obj > latest_per_device[serial]['_dt']:
            # Store record along with parsed datetime for comparison
            rcopy = dict(record)
            rcopy['_dt'] = dt_obj
            latest_per_device[serial] = rcopy

    # Step 2: Count how many devices run each (device_name, version)
    combo_counts = defaultdict(int)
    for device_data in latest_per_device.values():
        device_name = device_data.get('device_name', '')
        version = device_data.get('version', '')
        combo_counts[(device_name, version)] += 1

    # Step 3: Create summary rows sorted by device_name then version
    summary_rows = []
    for (dev_name, ver), cnt in sorted(combo_counts.items()):
        summary_rows.append({
            "device_name": dev_name,
            "version": ver,
            "count": cnt
        })

    # Step 4: Add total row
    total_count = sum(item['count'] for item in summary_rows)
    summary_rows.append({
        "device_name": "**Total**",
        "version": "",
        "count": total_count
    })

    return summary_rows


def generate_device_summary(joined_records: List[Dict]) -> List[Dict]:
    """
    Generate a summary table for unique device counts by serial numbers.
    Serial numbers are globally unique, so we only count each serial_number once.

    Args:
        joined_records (List[Dict]): List of joined records.

    Returns:
        List[Dict]: Summary table rows with keys: device_name, count.
    """
    device_serial_map = {}
    seen_serials = set()  # Track seen serial numbers globally

    for record in joined_records:
        device_name = record.get('device_name', '')
        serial_number = record.get('serial_number', None)

        # Skip if missing either device_name or serial_number
        if not device_name or not serial_number:
            continue

        # Only count this serial_number once globally
        if serial_number in seen_serials:
            continue

        seen_serials.add(serial_number)
        device_serial_map[device_name] = device_serial_map.get(device_name, 0) + 1

    # Create summary rows
    summary_rows = [{"device_name": device, "count": count} for device, count in device_serial_map.items()]
    total_count = sum(count for count in device_serial_map.values())
    summary_rows.append({"device_name": "Total", "count": total_count})

    return summary_rows


def write_summary_table(summary_table: List[Dict], output_path: str, table_title: str = "Summary"):
    """
    Write a summary table to a Markdown file.

    Args:
        summary_table (List[Dict]): List of summary rows.
        output_path (str): Path to the Markdown file.
        table_title (str): Title of the summary table for logging.
    """
    markdown_table = tabulate(summary_table, headers="keys", tablefmt="github")
    with open(output_path, "w") as f:
        f.write(markdown_table)
    logging.info(f"{table_title} written to {output_path}:\n{markdown_table}")


def format_summary(joined_records: List[Dict]) -> str:
    """
    Format the summary tables using Jinja templates.

    For the version summary:
    - Uses generate_version_summary() to get the latest version per device.
    - total_devices is the count of these rows.

    For the device summary:
    - Uses generate_device_summary() which counts unique devices by serial_number.

    Returns:
        str: Combined summary in Markdown format.
    """
    # Generate version summary
    version_summary = generate_version_summary(joined_records)
    total_devices = len(version_summary)
    version_summary_md = render_template("version_summary.j2", {
        "version_summary": version_summary,
        "total_devices": total_devices
    })

    # Generate device summary
    device_summary = generate_device_summary(joined_records)
    device_summary_md = render_template("device_summary.j2", {
        "device_summary": device_summary
    })

    # Combine summaries
    return "\n\n".join([version_summary_md, device_summary_md])


def write_summary(summary_content: str, summary_file: str = None):
    """
    Write the formatted summary to a file or stdout.

    Args:
        summary_content (str): The formatted summary content.
        summary_file (str): The file to write the summary to. If None, outputs to stdout.
    """
    if summary_file:
        with open(summary_file, "w") as f:
            f.write(summary_content)
        logging.info(f"Summary written to {summary_file}")
    else:
        print(summary_content)


def output_summary(joined_records: List[Dict], summary_file: str = None):
    """
    Generate and output summaries to stdout or a file.

    Args:
        joined_records (List[Dict]): List of joined records.
        summary_file (str): Filename to write summaries. If None, outputs to stdout.
    """
    # Generate summary content
    summary_content = format_summary(joined_records)

    # Write summary to file or stdout
    write_summary(summary_content, summary_file)
