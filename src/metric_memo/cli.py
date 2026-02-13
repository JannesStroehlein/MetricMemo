import argparse

from .app import MetricMemoApp
from .commands.send_email import run_send_email
from .commands.template_preview import run_template_preview
from .config.settings import Settings


def main():
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

    args = parser.parse_args()

    try:
        app_settings = Settings()
    except Exception as e:
        print(f"Framework Error: Failed to load settings. {e}")
        raise SystemExit(1) from e

    app = MetricMemoApp(app_settings, args.time)

    if not args.command:
        parser.print_help()
        return

    if args.command == "send-email":
        try:
            run_send_email(app, args.template_path, args.subject_template)
            print("Report sent!")
        except Exception as e:
            print(f"Error sending email: {e}")
        return

    if args.command == "template-dev-server":
        try:
            run_template_preview(app, args.template_path, args.port)
        except KeyboardInterrupt:
            print("\nServer stopped.")
