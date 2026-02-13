"""
This module defines the settings for the application, including SMTP and remote API configurations.
"""
from typing import Annotated
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field, BeforeValidator

def split_comma_separated(v):
    """
    A validator function to split a comma-separated string into a list of strings.
    """
    if isinstance(v, str):
        return [item.strip() for item in v.split(",") if item.strip()]
    return v

class SmtpSettings(BaseModel):
    """
    The settings for connecting to an SMTP server for sending emails.
    """
    host: str = Field(..., description="SMTP server address")
    port: int | None = Field(
        None, description="SMTP server port (optional, default is 25 for non-TLS and 587 for TLS)")
    from_name: str = Field(
        "Reporter", description="Name to display in the 'From' field of the email")
    user: str = Field(..., description="SMTP username")
    password: str = Field(..., description="SMTP password")
    use_ssl: bool = Field(False, description="Whether to use SSL for SMTP connection")
    use_starttls: bool = Field(
        False, description="Whether to use STARTTLS for SMTP connection")

class RemoteApiSettings(BaseModel):
    """
    The settings for connecting to a remote API (e.g., Prometheus or Loki).
    """
    url: str = Field(..., description="API server URL")
    use_auth: bool = Field(
        False, description="Whether to use authentication for the API")
    user: str | None = Field(
        None, description="API username (required if use_auth is True)")
    password: str | None = Field(
        None, description="API password (required if use_auth is True)")

class Settings(BaseSettings):
    """
    The runtime settings of the application.
    """
    # Prometheus
    prom: RemoteApiSettings = Field(..., description="Settings for Prometheus API")

    # Loki
    loki: RemoteApiSettings = Field(..., description="Settings for Loki API")

    # SMTP
    smtp: SmtpSettings = Field(..., description="Settings for SMTP server")
    recipients: Annotated[str | list[str], BeforeValidator(split_comma_separated)] = Field(
        ..., description="Recipient email addresses separated by commas"
    )

    # Configuration for loading .env files
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        env_prefix="METRIC_MEMO_", # Allows settings to be prefixed with METRIC_MEMO_ in .env
        case_sensitive=False, # Allows PROM_URL to map to prom_url
        extra="ignore"
    )
