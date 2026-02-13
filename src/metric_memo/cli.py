"""
This module contains the command-line interface for the Metric Memo application.
"""
import argparse


parser = argparse.ArgumentParser(prog="metric-memo")
parser.add_argument(
    "-t",
    "--time",
    default="7d",
    help="Set the time selection for the stats (24h, 7d)",
)
parser.add_argument(
    "--template-path",
    default="templates/weekly.html.jinja",
    help="Set the template path to use for the report",
)

commands = parser.add_subparsers(title="sub-commands", dest="command")

mail_parser = commands.add_parser("send-email", help="Send the email report")
mail_parser.add_argument(
    "--subject-template",
    default="Weekly Infrastructure Report - {{ date }}",
    help="Set a custom subject template for the email report",
)

dev_parser = commands.add_parser(
    "template-dev-server",
    help="Start a local HTTP server to serve the template output for development",
)
dev_parser.add_argument(
    "--port", type=int, default=8000, help="Port for the dev server (default: 8000)"
)

def parse_args() -> argparse.Namespace:
    """
    Parses the command-line arguments and returns them as a Namespace object.
    """
    return parser.parse_args()

def print_help():
    """
    Prints the help message for the command-line interface.
    """
    parser.print_help()
