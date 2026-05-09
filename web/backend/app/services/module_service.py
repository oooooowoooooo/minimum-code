"""Module lookup and content assembly."""
from app.core.paths import PROJECT_ROOT
from app.repositories import json_repository
from app.schemas.module import ModuleContent, ModuleInfo, Section
from app.services import section_extractor


def _load_module_rows() -> list[dict]:
    data = json_repository.read_json("modules.json", default={"modules": []})
    if isinstance(data, dict):
        return data.get("modules", [])
    return []


def list_modules() -> list[ModuleInfo]:
    """List all public module summaries."""
    return [ModuleInfo(**module) for module in _load_module_rows()]


def get_module_row(module_id: str) -> dict | None:
    """Return the raw module row so services can access non-public fields."""
    return next((module for module in _load_module_rows() if module.get("id") == module_id), None)


def module_count() -> int:
    """Return the total number of configured modules."""
    return len(_load_module_rows())


def get_module_sections(module_id: str) -> list[Section]:
    """Extract learning sections for a module from its configured source file."""
    module = get_module_row(module_id)
    if not module:
        return []

    source_path = module.get("source_path")
    if not source_path:
        return []

    return section_extractor.extract_sections(PROJECT_ROOT / source_path)


def get_module_content(module_id: str) -> ModuleContent | None:
    """Build complete module content for the API layer."""
    module = get_module_row(module_id)
    if not module:
        return None

    sections = get_module_sections(module_id)
    if not sections:
        sections = [
            Section(title="Overview", content=f"This module covers {module['title']}.", type="text"),
            Section(
                title="Key Concepts",
                content="Refer to the source files in the project for detailed content.",
                type="text",
            ),
        ]

    return ModuleContent(
        id=module["id"],
        title=module["title"],
        category=module["category"],
        icon=module["icon"],
        sections=sections,
    )
