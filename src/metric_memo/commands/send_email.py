from src.metric_memo.app import MetricMemoApp


def run_send_email(app: MetricMemoApp, template_path: str, subject_template: str):
    subject = app.render_email_subject(subject_template)
    app.send_email(template_path, subject)
