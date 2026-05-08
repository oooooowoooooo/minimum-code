"""Interview expression generation service."""
from app.repositories import json_repository


def load_labs_data() -> dict:
    """Load labs data from data file."""
    return json_repository.read_json("labs.json", default={"labs": []})


def generate_expressions(completed_labs: list[str], target_role: str) -> list[dict]:
    """Generate interview expressions from completed labs.

    Uses labs.json data if available, otherwise returns mock expressions.
    """
    labs_data = load_labs_data()
    labs_list = labs_data.get("labs", [])
    labs_by_id = {lab["id"]: lab for lab in labs_list}

    expressions = []
    for lab_id in completed_labs:
        lab = labs_by_id.get(lab_id)
        if lab:
            expressions.append({
                "lab_id": lab_id,
                "title": lab.get("title", lab_id),
                "bullet_points": [
                    f"Implemented {lab.get('title', lab_id)} as part of the {target_role} learning path",
                    f"Applied {lab.get('difficulty', 'intermediate')}-level concepts in a hands-on project",
                    f"Delivered working solution meeting all acceptance criteria",
                ],
                "star_method": {
                    "situation": f"During the AI Era learning platform curriculum, I was assigned the {lab.get('title', lab_id)} lab.",
                    "task": f"Build a functional {lab.get('title', lab_id).lower()} that demonstrates core {target_role} competencies.",
                    "action": f"Designed the architecture, implemented the solution with proper error handling, and verified against acceptance criteria.",
                    "result": f"Successfully completed the lab, gaining practical experience applicable to {target_role} roles.",
                },
            })
        else:
            # Mock expression for unknown lab IDs
            expressions.append({
                "lab_id": lab_id,
                "title": lab_id.replace("-", " ").title(),
                "bullet_points": [
                    f"Completed {lab_id} lab demonstrating hands-on {target_role} skills",
                    "Applied software engineering best practices including testing and documentation",
                ],
                "star_method": {
                    "situation": f"I was tasked with completing the {lab_id} lab in the AI Era curriculum.",
                    "task": f"Build a working implementation that demonstrates key {target_role} concepts.",
                    "action": "Analyzed requirements, designed the solution, implemented iteratively, and tested thoroughly.",
                    "result": f"Delivered a working solution and deepened practical {target_role} expertise.",
                },
            })

    return expressions
