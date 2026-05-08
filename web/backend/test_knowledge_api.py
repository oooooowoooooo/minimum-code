"""
Tests for knowledge-point API endpoints.
Uses Starlette TestClient (bundled with FastAPI) — no extra deps needed.
"""

import json
import pytest
from starlette.testclient import TestClient

from main import app


@pytest.fixture(scope="module")
def client():
    """Shared TestClient for all tests in this module."""
    with TestClient(app) as c:
        yield c


# ============================================================================
# VALID GAME TYPES AND THEIR REQUIRED CONTENT KEYS
# ============================================================================

VALID_GAME_TYPES = {
    "predict_output": {"code", "options", "correct", "explanation"},
    "find_bug": {"code_lines", "bug_line", "explanation"},
    "fill_blank": {"code", "blanks", "explanation"},
    "code_order": {"lines", "correct_order", "explanation"},
}

REQUIRED_POINT_FIELDS = ["week", "module", "title", "explanation", "code", "game", "quiz"]


# ============================================================================
# Helper: get ALL points (paginate through everything)
# ============================================================================

def get_all_points(client) -> list[dict]:
    """Fetch every knowledge point across all pages."""
    all_points = []
    page = 1
    while True:
        data = client.get("/api/knowledge-points", params={"page": page, "per_page": 100}).json()
        batch = data.get("points", [])
        if not batch:
            break
        all_points.extend(batch)
        if len(all_points) >= data["total"]:
            break
        page += 1
    return all_points


# ============================================================================
# 1. GET /api/knowledge-points — basic list + pagination
# ============================================================================

class TestListKnowledgePoints:
    def test_returns_200_and_valid_json(self, client):
        resp = client.get("/api/knowledge-points")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, dict)

    def test_expected_fields_exist(self, client):
        data = client.get("/api/knowledge-points").json()
        assert "total" in data
        assert "page" in data
        assert "per_page" in data
        assert "pages" in data
        assert "points" in data

    def test_data_types(self, client):
        data = client.get("/api/knowledge-points").json()
        assert isinstance(data["total"], int)
        assert isinstance(data["page"], int)
        assert isinstance(data["per_page"], int)
        assert isinstance(data["pages"], int)
        assert isinstance(data["points"], list)

    def test_total_is_positive(self, client):
        data = client.get("/api/knowledge-points").json()
        assert data["total"] > 0

    def test_point_has_expected_keys(self, client):
        data = client.get("/api/knowledge-points").json()
        point = data["points"][0]
        assert "week" in point
        assert "module" in point
        assert "title" in point


# ============================================================================
# 2. GET /api/knowledge-points?search=xxx
# ============================================================================

class TestSearchKnowledgePoints:
    def test_search_returns_200(self, client):
        resp = client.get("/api/knowledge-points", params={"search": "program"})
        assert resp.status_code == 200

    def test_search_returns_results(self, client):
        data = client.get("/api/knowledge-points", params={"search": "program"}).json()
        assert data["total"] > 0
        assert len(data["points"]) > 0

    def test_search_results_contain_term(self, client):
        """Every result must have the search term in title or explanation."""
        data = client.get("/api/knowledge-points", params={"search": "function"}).json()
        for p in data["points"]:
            in_title = "function" in p["title"].lower()
            in_explanation = "function" in p["explanation"].lower()
            assert in_title or in_explanation, (
                f"Point '{p['title']}' does not contain 'function' in title or explanation"
            )

    def test_search_is_case_insensitive(self, client):
        lower = client.get("/api/knowledge-points", params={"search": "variable"}).json()
        upper = client.get("/api/knowledge-points", params={"search": "VARIABLE"}).json()
        assert lower["total"] == upper["total"]

    def test_search_no_results(self, client):
        data = client.get("/api/knowledge-points", params={"search": "xyznonexistent123"}).json()
        assert data["total"] == 0
        assert data["points"] == []

    def test_search_combined_with_week(self, client):
        data = client.get(
            "/api/knowledge-points",
            params={"search": "program", "week": 1},
        ).json()
        for p in data["points"]:
            assert p["week"] == 1


# ============================================================================
# 3. GET /api/knowledge-points/random?count=5
# ============================================================================

class TestRandomKnowledgePoints:
    def test_random_returns_200(self, client):
        resp = client.get("/api/knowledge-points/random", params={"count": 5})
        assert resp.status_code == 200

    def test_random_returns_expected_count(self, client):
        data = client.get("/api/knowledge-points/random", params={"count": 5}).json()
        assert data["count"] == 5
        assert len(data["points"]) == 5

    def test_random_default_count(self, client):
        """Default count should be 10."""
        data = client.get("/api/knowledge-points/random").json()
        assert data["count"] == 10
        assert len(data["points"]) == 10

    def test_random_count_clamped_to_max(self, client):
        """Count should be clamped to max 100."""
        data = client.get("/api/knowledge-points/random", params={"count": 999}).json()
        assert data["count"] <= 100

    def test_random_points_have_valid_structure(self, client):
        data = client.get("/api/knowledge-points/random", params={"count": 3}).json()
        for p in data["points"]:
            for field in REQUIRED_POINT_FIELDS:
                assert field in p, f"Missing field '{field}' in random point"


# ============================================================================
# 4. GET /api/knowledge-points/id/0 (single point by index)
# ============================================================================

class TestSingleKnowledgePoint:
    def test_single_point_returns_200(self, client):
        resp = client.get("/api/knowledge-points/id/0")
        assert resp.status_code == 200

    def test_single_point_structure(self, client):
        data = client.get("/api/knowledge-points/id/0").json()
        assert "id" in data
        assert "point" in data
        assert data["id"] == 0

    def test_single_point_has_all_fields(self, client):
        data = client.get("/api/knowledge-points/id/0").json()
        point = data["point"]
        for field in REQUIRED_POINT_FIELDS:
            assert field in point, f"Missing required field '{field}'"

    def test_single_point_out_of_range_returns_404(self, client):
        resp = client.get("/api/knowledge-points/id/99999")
        assert resp.status_code == 404


# ============================================================================
# 5. Pagination with large datasets
# ============================================================================

class TestPagination:
    def test_pagination_respects_per_page(self, client):
        data = client.get("/api/knowledge-points", params={"per_page": 3}).json()
        assert len(data["points"]) <= 3
        assert data["per_page"] == 3

    def test_pagination_page_numbers(self, client):
        page1 = client.get("/api/knowledge-points", params={"page": 1, "per_page": 5}).json()
        page2 = client.get("/api/knowledge-points", params={"page": 2, "per_page": 5}).json()
        assert page1["page"] == 1
        assert page2["page"] == 2

    def test_pagination_different_pages_different_data(self, client):
        """Points on page 1 should not overlap with page 2."""
        page1 = client.get("/api/knowledge-points", params={"page": 1, "per_page": 5}).json()
        page2 = client.get("/api/knowledge-points", params={"page": 2, "per_page": 5}).json()
        titles_p1 = {p["title"] for p in page1["points"]}
        titles_p2 = {p["title"] for p in page2["points"]}
        assert titles_p1.isdisjoint(titles_p2)

    def test_pagination_pages_calculated_correctly(self, client):
        data = client.get("/api/knowledge-points", params={"per_page": 10}).json()
        total = data["total"]
        expected_pages = (total + 9) // 10  # ceiling division
        assert data["pages"] == expected_pages

    def test_pagination_empty_beyond_last_page(self, client):
        data = client.get("/api/knowledge-points", params={"page": 9999, "per_page": 20}).json()
        assert data["points"] == []

    def test_pagination_full_dataset(self, client):
        """Fetching all pages yields exactly total number of points."""
        all_pts = get_all_points(client)
        total = client.get("/api/knowledge-points").json()["total"]
        assert len(all_pts) == total

    def test_all_points_unique(self, client):
        """No duplicate points across pages."""
        all_pts = get_all_points(client)
        titles = [p["title"] for p in all_pts]
        assert len(titles) == len(set(titles))


# ============================================================================
# 6. Verify game field is structured JSON (has 'type' key)
# ============================================================================

class TestGameFieldStructure:
    def test_every_point_has_game(self, client):
        all_pts = get_all_points(client)
        for p in all_pts:
            assert "game" in p, f"Point '{p['title']}' missing 'game' field"

    def test_game_is_dict(self, client):
        all_pts = get_all_points(client)
        for p in all_pts:
            assert isinstance(p["game"], dict), (
                f"Point '{p['title']}': game should be dict, got {type(p['game']).__name__}"
            )

    def test_game_has_type_key(self, client):
        all_pts = get_all_points(client)
        for p in all_pts:
            assert "type" in p["game"], (
                f"Point '{p['title']}': game missing 'type' key"
            )

    def test_game_type_is_valid(self, client):
        all_pts = get_all_points(client)
        for p in all_pts:
            gt = p["game"]["type"]
            assert gt in VALID_GAME_TYPES, (
                f"Point '{p['title']}': unknown game type '{gt}'"
            )

    def test_game_has_title(self, client):
        all_pts = get_all_points(client)
        for p in all_pts:
            assert "title" in p["game"], f"Point '{p['title']}': game missing 'title'"

    def test_game_has_instructions(self, client):
        all_pts = get_all_points(client)
        for p in all_pts:
            assert "instructions" in p["game"], f"Point '{p['title']}': game missing 'instructions'"

    def test_game_has_content(self, client):
        all_pts = get_all_points(client)
        for p in all_pts:
            assert "content" in p["game"], f"Point '{p['title']}': game missing 'content'"
            assert isinstance(p["game"]["content"], dict), (
                f"Point '{p['title']}': game.content should be dict"
            )


# ============================================================================
# 7. Verify all points have required fields
# ============================================================================

class TestRequiredFields:
    def test_all_points_have_required_fields(self, client):
        all_pts = get_all_points(client)
        assert len(all_pts) > 0
        for p in all_pts:
            for field in REQUIRED_POINT_FIELDS:
                assert field in p, (
                    f"Point '{p.get('title', '?')}' missing required field '{field}'"
                )

    def test_week_is_positive_int(self, client):
        all_pts = get_all_points(client)
        for p in all_pts:
            assert isinstance(p["week"], int)
            assert p["week"] >= 1

    def test_module_is_nonempty_string(self, client):
        all_pts = get_all_points(client)
        for p in all_pts:
            assert isinstance(p["module"], str)
            assert len(p["module"]) > 0

    def test_title_is_nonempty_string(self, client):
        all_pts = get_all_points(client)
        for p in all_pts:
            assert isinstance(p["title"], str)
            assert len(p["title"]) > 0

    def test_explanation_is_nonempty_string(self, client):
        all_pts = get_all_points(client)
        for p in all_pts:
            assert isinstance(p["explanation"], str)
            assert len(p["explanation"]) > 0

    def test_code_is_string(self, client):
        all_pts = get_all_points(client)
        for p in all_pts:
            assert isinstance(p["code"], str)


# ============================================================================
# 8. Verify quiz has 4 options
# ============================================================================

class TestQuizStructure:
    def test_quiz_exists_on_all_points(self, client):
        all_pts = get_all_points(client)
        for p in all_pts:
            assert "quiz" in p, f"Point '{p['title']}' missing 'quiz'"

    def test_quiz_is_dict(self, client):
        all_pts = get_all_points(client)
        for p in all_pts:
            assert isinstance(p["quiz"], dict), (
                f"Point '{p['title']}': quiz should be dict"
            )

    def test_quiz_has_question(self, client):
        all_pts = get_all_points(client)
        for p in all_pts:
            assert "question" in p["quiz"], f"Point '{p['title']}': quiz missing 'question'"

    def test_quiz_has_options(self, client):
        all_pts = get_all_points(client)
        for p in all_pts:
            assert "options" in p["quiz"], f"Point '{p['title']}': quiz missing 'options'"

    def test_quiz_has_exactly_4_options(self, client):
        all_pts = get_all_points(client)
        for p in all_pts:
            opts = p["quiz"]["options"]
            assert len(opts) == 4, (
                f"Point '{p['title']}': quiz has {len(opts)} options, expected 4"
            )

    def test_quiz_options_are_strings(self, client):
        all_pts = get_all_points(client)
        for p in all_pts:
            for i, opt in enumerate(p["quiz"]["options"]):
                assert isinstance(opt, str), (
                    f"Point '{p['title']}': quiz option {i} is not a string"
                )

    def test_quiz_has_correct_field(self, client):
        all_pts = get_all_points(client)
        for p in all_pts:
            assert "correct" in p["quiz"], f"Point '{p['title']}': quiz missing 'correct'"

    def test_quiz_correct_is_valid_index(self, client):
        all_pts = get_all_points(client)
        for p in all_pts:
            correct = p["quiz"]["correct"]
            assert isinstance(correct, int)
            assert 0 <= correct < len(p["quiz"]["options"]), (
                f"Point '{p['title']}': quiz.correct={correct} out of range"
            )

    def test_quiz_has_explanation(self, client):
        all_pts = get_all_points(client)
        for p in all_pts:
            assert "explanation" in p["quiz"], (
                f"Point '{p['title']}': quiz missing 'explanation'"
            )


# ============================================================================
# 9. Verify game content structure matches its type
# ============================================================================

class TestGameContentByType:
    def test_predict_output_has_required_content_keys(self, client):
        all_pts = get_all_points(client)
        po_points = [p for p in all_pts if p["game"]["type"] == "predict_output"]
        assert len(po_points) > 0, "No predict_output games found"
        for p in po_points:
            c = p["game"]["content"]
            assert "code" in c, f"'{p['title']}': predict_output missing 'code'"
            assert "options" in c, f"'{p['title']}': predict_output missing 'options'"
            assert "correct" in c, f"'{p['title']}': predict_output missing 'correct'"
            assert "explanation" in c, f"'{p['title']}': predict_output missing 'explanation'"
            assert isinstance(c["options"], list)
            assert isinstance(c["correct"], int)

    def test_find_bug_has_required_content_keys(self, client):
        all_pts = get_all_points(client)
        fb_points = [p for p in all_pts if p["game"]["type"] == "find_bug"]
        assert len(fb_points) > 0, "No find_bug games found"
        for p in fb_points:
            c = p["game"]["content"]
            assert "code_lines" in c, f"'{p['title']}': find_bug missing 'code_lines'"
            assert "bug_line" in c, f"'{p['title']}': find_bug missing 'bug_line'"
            assert "explanation" in c, f"'{p['title']}': find_bug missing 'explanation'"
            assert isinstance(c["code_lines"], list)
            assert isinstance(c["bug_line"], int)

    def test_fill_blank_has_required_content_keys(self, client):
        all_pts = get_all_points(client)
        fb_points = [p for p in all_pts if p["game"]["type"] == "fill_blank"]
        assert len(fb_points) > 0, "No fill_blank games found"
        for p in fb_points:
            c = p["game"]["content"]
            assert "code" in c, f"'{p['title']}': fill_blank missing 'code'"
            assert "blanks" in c, f"'{p['title']}': fill_blank missing 'blanks'"
            assert "explanation" in c, f"'{p['title']}': fill_blank missing 'explanation'"
            assert isinstance(c["blanks"], list)
            assert len(c["blanks"]) > 0
            # Each blank should have position, answer, options
            for blank in c["blanks"]:
                assert "position" in blank, f"'{p['title']}': blank missing 'position'"
                assert "answer" in blank, f"'{p['title']}': blank missing 'answer'"

    def test_code_order_has_required_content_keys(self, client):
        all_pts = get_all_points(client)
        co_points = [p for p in all_pts if p["game"]["type"] == "code_order"]
        assert len(co_points) > 0, "No code_order games found"
        for p in co_points:
            c = p["game"]["content"]
            assert "lines" in c, f"'{p['title']}': code_order missing 'lines'"
            assert "correct_order" in c, f"'{p['title']}': code_order missing 'correct_order'"
            assert "explanation" in c, f"'{p['title']}': code_order missing 'explanation'"
            assert isinstance(c["lines"], list)
            assert isinstance(c["correct_order"], list)
            assert len(c["lines"]) == len(c["correct_order"]), (
                f"'{p['title']}': lines count != correct_order count"
            )

    def test_all_game_types_present(self, client):
        """Ensure the dataset covers all 4 expected game types."""
        all_pts = get_all_points(client)
        found_types = {p["game"]["type"] for p in all_pts}
        for gt in VALID_GAME_TYPES:
            assert gt in found_types, f"Game type '{gt}' not found in dataset"


# ============================================================================
# 10. Filter by week
# ============================================================================

class TestFilterByWeek:
    def test_returns_200(self, client):
        resp = client.get("/api/knowledge-points", params={"week": 1})
        assert resp.status_code == 200

    def test_all_points_belong_to_week_1(self, client):
        data = client.get("/api/knowledge-points", params={"week": 1}).json()
        for p in data["points"]:
            assert p["week"] == 1

    def test_returns_some_results(self, client):
        data = client.get("/api/knowledge-points", params={"week": 1}).json()
        assert data["total"] > 0
        assert len(data["points"]) > 0


# ============================================================================
# 11. Filter by module
# ============================================================================

class TestFilterByModule:
    def test_returns_200(self, client):
        resp = client.get("/api/knowledge-points", params={"module": "cognitive-why"})
        assert resp.status_code == 200

    def test_all_points_belong_to_module(self, client):
        data = client.get(
            "/api/knowledge-points", params={"module": "cognitive-why"}
        ).json()
        for p in data["points"]:
            assert p["module"] == "cognitive-why"

    def test_returns_some_results(self, client):
        data = client.get(
            "/api/knowledge-points", params={"module": "cognitive-why"}
        ).json()
        assert data["total"] > 0


# ============================================================================
# 12. Combined filters
# ============================================================================

class TestCombinedFilter:
    def test_returns_200(self, client):
        resp = client.get(
            "/api/knowledge-points",
            params={"week": 1, "module": "cognitive-why"},
        )
        assert resp.status_code == 200

    def test_all_points_match_both_filters(self, client):
        data = client.get(
            "/api/knowledge-points",
            params={"week": 1, "module": "cognitive-why"},
        ).json()
        for p in data["points"]:
            assert p["week"] == 1
            assert p["module"] == "cognitive-why"

    def test_fewer_or_equal_results_than_week_alone(self, client):
        all_week = client.get(
            "/api/knowledge-points", params={"week": 1}
        ).json()
        combined = client.get(
            "/api/knowledge-points",
            params={"week": 1, "module": "cognitive-why"},
        ).json()
        assert combined["total"] <= all_week["total"]


# ============================================================================
# 13. Stats endpoint
# ============================================================================

class TestKnowledgePointsStats:
    def test_returns_200_and_json(self, client):
        resp = client.get("/api/knowledge-points/stats")
        assert resp.status_code == 200
        assert isinstance(resp.json(), dict)

    def test_expected_fields(self, client):
        data = client.get("/api/knowledge-points/stats").json()
        assert "total_points" in data
        assert "points_per_week" in data
        assert "points_per_module" in data

    def test_data_types(self, client):
        data = client.get("/api/knowledge-points/stats").json()
        assert isinstance(data["total_points"], int)
        assert isinstance(data["points_per_week"], dict)
        assert isinstance(data["points_per_module"], dict)

    def test_total_points_positive(self, client):
        data = client.get("/api/knowledge-points/stats").json()
        assert data["total_points"] > 0

    def test_stats_total_matches_list_total(self, client):
        stats = client.get("/api/knowledge-points/stats").json()
        listing = client.get("/api/knowledge-points").json()
        assert stats["total_points"] == listing["total"]


# ============================================================================
# 14. Weeks endpoint
# ============================================================================

class TestWeeksEndpoint:
    def test_returns_200_and_json(self, client):
        resp = client.get("/api/weeks")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)

    def test_week_entry_structure(self, client):
        data = client.get("/api/weeks").json()
        assert len(data) > 0
        entry = data[0]
        assert "week" in entry
        assert "modules" in entry
        assert "total_points" in entry

    def test_week_entry_types(self, client):
        data = client.get("/api/weeks").json()
        entry = data[0]
        assert isinstance(entry["week"], int)
        assert isinstance(entry["modules"], list)
        assert isinstance(entry["total_points"], int)

    def test_module_entry_structure(self, client):
        data = client.get("/api/weeks").json()
        mod = data[0]["modules"][0]
        assert "module" in mod
        assert "count" in mod


# ============================================================================
# 15. Modules endpoints
# ============================================================================

class TestListModules:
    def test_returns_200_and_json(self, client):
        resp = client.get("/api/modules")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_module_entry_fields(self, client):
        data = client.get("/api/modules").json()
        assert len(data) > 0
        mod = data[0]
        assert "id" in mod
        assert "title" in mod
        assert "category" in mod
        assert "icon" in mod
        assert "description" in mod
        assert "week" in mod
        assert "order" in mod

    def test_contains_cognitive_why(self, client):
        data = client.get("/api/modules").json()
        ids = [m["id"] for m in data]
        assert "cognitive-why" in ids


class TestGetModule:
    def test_returns_200_and_json(self, client):
        resp = client.get("/api/modules/cognitive-why")
        assert resp.status_code == 200
        assert isinstance(resp.json(), dict)

    def test_expected_fields(self, client):
        data = client.get("/api/modules/cognitive-why").json()
        assert data["id"] == "cognitive-why"
        assert "title" in data
        assert "category" in data
        assert "icon" in data
        assert "sections" in data

    def test_sections_is_list(self, client):
        data = client.get("/api/modules/cognitive-why").json()
        assert isinstance(data["sections"], list)
        assert len(data["sections"]) > 0

    def test_section_structure(self, client):
        data = client.get("/api/modules/cognitive-why").json()
        sec = data["sections"][0]
        assert "title" in sec
        assert "content" in sec
        assert "type" in sec


# ============================================================================
# 16. Quiz endpoints (old-style module quizzes)
# ============================================================================

class TestGetQuiz:
    def test_returns_200_and_json(self, client):
        resp = client.get("/api/modules/cognitive-why/quiz")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    def test_quiz_entry_structure(self, client):
        data = client.get("/api/modules/cognitive-why/quiz").json()
        assert len(data) > 0
        q = data[0]
        assert "question" in q
        assert "options" in q
        assert "correct" in q
        assert "explanation" in q

    def test_quiz_entry_types(self, client):
        data = client.get("/api/modules/cognitive-why/quiz").json()
        q = data[0]
        assert isinstance(q["question"], str)
        assert isinstance(q["options"], list)
        assert isinstance(q["correct"], int)
        assert isinstance(q["explanation"], str)


# ============================================================================
# 17. Progress endpoints
# ============================================================================

class TestProgress:
    def test_returns_200_and_json(self, client):
        resp = client.get("/api/progress")
        assert resp.status_code == 200
        assert isinstance(resp.json(), dict)

    def test_expected_fields(self, client):
        data = client.get("/api/progress").json()
        assert "completed" in data

    def test_completed_is_list(self, client):
        data = client.get("/api/progress").json()
        assert isinstance(data["completed"], list)
