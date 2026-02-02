# Prometheus & Loki Reporting Tool

This tool can generate and send HTML email reports based on data queried from Prometheus and Loki. It supports customizable email templates and includes a development server for template testing.

## CLI Usage

This tool provides a command-line interface (CLI) with the following commands:

- `send-email`: Sends the email report using the specified template.
  - `--subject-template`: (Optional) Set a custom subject template for the email report. Default is `Weekly Infrastructure Report - {{ date }}`.
- `template-dev-server`: Starts a local HTTP server to serve the template output for development.
  - `--port`: (Optional) Port for the dev server (default: `8000`).

### Global Arguments

Some arguments are applicable to all commands:

- `--template-path`: Path to the Jinja2 HTML template file relative to `./templates` (default: `weekly.html.jinja`).
- `-t, --time-selection`: Time range for the report data (default: `7d`).

### Example Commands

Send an email report with a custom subject:

```bash
python main.py send-email --subject-template "Custom Report - {{ date }}"
```

Start the template development server on a specific port:

```bash
python main.py template-dev-server --port 8080
```

## Environment Variables

The tool requires the following environment variables to be set for email functionality. They can also be defined in a `.env` file:

| Environment Variable | Description                                          |
| -------------------- | ---------------------------------------------------- |
| `EMAIL_TO`           | Recipient email address                              |
| `SMTP_HOST`          | SMTP server host                                     |
| `SMTP_PORT`          | SMTP server port                                     |
| `SMTP_USER`          | SMTP username                                        |
| `SMTP_PASSWORD`      | SMTP password                                        |
| `SMTP_FROM_NAME`     | Name to display in the "From" field                  |
| `SMTP_USE_TLS`       | Use TLS for SMTP connection (true/false)             |
| `SMTP_USE_SSL`       | Use SSL for SMTP connection (true/false)             |
| `LOKI_URL`           | Loki server URL                                      |
| `LOKI_USE_AUTH`      | Use basic authentication for Loki (true/false)       |
| `LOKI_USER`          | Loki username                                        |
| `LOKI_PASS`          | Loki password                                        |
| `PROM_URL`           | Prometheus server URL                                |
| `PROM_USE_AUTH`      | Use basic authentication for Prometheus (true/false) |
| `PROM_USER`          | Prometheus username                                  |
| `PROM_PASS`          | Prometheus password                                  |


## Jinja2 Template

The email report is generated using a Jinja2 HTML template. You can customize the template to fit your reporting needs. The default template file is `weekly.html.jinja`.
The template has access to the following variables:
- `time_selection`: The time range selected for the report (e.g., `7d`). This can be used in queries to Prometheus and Loki.
- `now`: The current UTC date and time as a datetime object.
- `date`: The current date in `YYYY-MM-DD` format.
- `start_date`: The start date of the selected time range.
- `end_date`: The end date of the selected time range.


### Functions
The following functions are available within the Jinja2 template for querying data:
- `query_prom(query: str)`: Executes a Prometheus query and returns the result as a single number (scalar).
- `query_prom_raw(query: str)`: Executes a Prometheus query and returns the raw result as a list (including labels and values).
- `query_loki(query: str)`: Executes a Loki query and returns a list of dictionaries `{message, count}`.
- `query_loki_top(selector: str, label: str, limit: int = 10)`: Executes a Top-N query for a specific label in Loki and returns a list of dictionaries `{label_value, count}`.
- `query_loki_raw(logql: str, limit: int = 50)`: Fetches raw log lines from Loki over the selected time window and returns a list of dictionaries `{timestamp, message, labels}`.

### Filters

The following custom filters are available within the Jinja2 template:
- `fmt_bytes(value)`: Converts a byte value into a human-readable format (e.g KB, MB, GB).
- `fmt_pct(value)`: Formats a float value as a percentage with two decimal places.
- `fmt_timedelta(value)`: Formats a timedelta value into a human-readable string (e.g., "2d 3h").
- `from_epoch(value)`: Converts an epoch timestamp to a human-readable date string.
- `to_timedelta(value)`: Converts a number of seconds into a timedelta object.