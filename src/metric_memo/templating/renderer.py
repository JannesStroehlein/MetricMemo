from pathlib import Path

from jinja2 import Environment, FileSystemLoader


class TemplateRenderer:
    def __init__(self, globals_: dict | None = None, filters: dict | None = None):
        self.globals = globals_ or {}
        self.filters = filters or {}

    @staticmethod
    def resolve_template_path(path: str) -> Path:
        candidate = Path(path).expanduser()

        if candidate.is_absolute():
            if candidate.is_file():
                return candidate
            raise FileNotFoundError(f"Template file not found: {candidate}")

        cwd_candidate = Path.cwd() / candidate
        if cwd_candidate.is_file():
            return cwd_candidate

        raise FileNotFoundError(
            f"Template file not found: {path}. Provide a valid absolute or relative path."
        )

    def _build_environment(self, template_path: Path) -> Environment:
        environment = Environment(
            autoescape=True,
            loader=FileSystemLoader(str(template_path.parent)),
        )
        environment.globals.update(self.globals)
        environment.filters.update(self.filters)
        return environment

    def render_file(self, path: str) -> str:
        template_path = self.resolve_template_path(path)
        environment = self._build_environment(template_path)
        template = environment.get_template(template_path.name)
        return template.render()

    def render_string(self, template_str: str) -> str:
        environment = Environment(autoescape=True)
        environment.globals.update(self.globals)
        environment.filters.update(self.filters)
        template = environment.from_string(template_str)
        return template.render()
