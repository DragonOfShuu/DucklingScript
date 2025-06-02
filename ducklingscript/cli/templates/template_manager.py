from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from pathlib import Path
from shutil import copytree


class TemplateClass(Enum):
    PLUGINS = "plugins"
    PROJECT = "project"


@dataclass
class Template:
    name: str
    directory: Path
    description: str | None
    template_class: TemplateClass


TemplatePresets = dict[TemplateClass, list[Template]]


class TemplateManager:
    def __init__(self):
        self.templates: TemplatePresets = {}

    @classmethod
    def get(cls):
        """Singleton instance of TemplateManager."""
        if not hasattr(cls, "_instance"):
            cls._instance = cls._create_default_template_manager()
        return cls._instance

    @classmethod
    def _create_default_template_manager(cls):
        instance = cls()
        temp = cls.default_template_directory()
        instance.add_template(
            TemplateClass.PLUGINS,
            "default",
            temp / "plugins",
            "Default plugin template",
        )
        return instance

    @staticmethod
    @lru_cache(maxsize=1)
    def default_template_directory() -> Path:
        """Return the default template directory."""
        return Path(__file__).absolute().parent

    def add_template(
        self,
        template_class: TemplateClass,
        name: str,
        parent_directory: Path,
        description: str | None = None,
    ):
        """Add a new template."""
        template = Template(
            name=name,
            directory=parent_directory / name,
            description=description,
            template_class=template_class,
        )
        self.add_template_class(template_class, template)

    def remove_template(self, template_class: TemplateClass, name: str) -> bool:
        """Remove a template by name and class."""
        if template_class not in self.templates:
            return False

        templates = self.templates[template_class]

        for i, template in enumerate(templates):
            if template.name != name:
                continue

            del templates[i]
            self.templates[template_class] = templates
            return True

        return False

    def add_template_class(self, template_class: TemplateClass, template: Template):
        """Add a new template."""
        self.templates[template_class] = self.templates.get(template_class, []) + [
            template
        ]

    def get_template(self, template_class: TemplateClass, name: str) -> Template | None:
        """Retrieve a template by name."""
        for template in self.templates.get(template_class, []):
            if template.name == name:
                return template
        return None

    def list_all_templates(self) -> list[Template]:
        """List all available templates."""
        return [
            template for templates in self.templates.values() for template in templates
        ]

    def list_templates_by_class(self, template_class: TemplateClass) -> list[Template]:
        """List templates by class."""
        return self.templates.get(template_class, [])

    def copy_template(self, template_path: Path, destination: Path):
        """Copy a template directory to a destination."""
        if not template_path.exists():
            raise FileNotFoundError(f"Template path {template_path} does not exist.")

        if not destination.exists():
            destination.mkdir(parents=True, exist_ok=True)

        copytree(template_path, destination, dirs_exist_ok=True)
