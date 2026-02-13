"""
This module contains the command for sending the email report.
"""
from metric_memo.app import RuntimeDependencies


def run_send_email(runtime: RuntimeDependencies, template_path: str, subject_template: str):
    """
    Renders the email subject and body using the provided templates and sends the email report.
    """
    subject = runtime.report_renderer.render_email_subject(subject_template)
    html_body = runtime.report_renderer.render_html(template_path)
    runtime.email_sender.send_html(runtime.settings.recipients, subject, html_body)
