"""Example 79: pytest Full Integration -- CRUD + token + pagination, one green suite (co-14, co-18, co-19)."""

import pytest  # => co-22: provides the @pytest.fixture decorator used below
from fastapi.testclient import TestClient  # => co-22: drives the app in-process, no real socket needed

from app import app  # => co-24: imports the SAME FastAPI instance app.py builds -- one process, no server

AUTH = {"Authorization": "Bearer s3cr3t-token-abc123"}  # => co-18: matches app.py's VALID_TOKEN exactly
BAD_AUTH = {"Authorization": "Bearer wrong-token"}  # => co-18: any string that is NOT VALID_TOKEN


@pytest.fixture()  # => co-22: reruns this function once per test that declares a "client" parameter
def client() -> TestClient:  # => co-22: a fresh client per test -- but the SQLite file persists across tests
    return TestClient(app)  # => co-22: wraps `app` for in-process requests, no uvicorn process needed


# -- CRUD group (co-14) ------------------------------------------------------------------
class TestCrud:  # => co-14: groups every create/read/update/delete assertion under one namespace
    def test_create_requires_a_token(self, client: TestClient) -> None:  # => co-18: guard check first
        response = client.post("/tasks", json={"title": "a"})  # => co-18: deliberately NO Authorization header
        assert response.status_code == 401  # => co-18: writes are guarded
        # => require_token raises BEFORE post_task's own body ever runs -- no row was created

    def test_create_read_update_delete_round_trip(self, client: TestClient) -> None:  # => co-14: full CRUD cycle
        created = client.post("/tasks", json={"title": "write the report"}, headers=AUTH)  # => co-18: valid token
        assert created.status_code == 201  # => co-03: 201 confirms a new resource now exists
        task_id = created.json()["id"]  # => co-14: the server-assigned id, read back from the response body
        # => every later call in this test reuses THIS id -- one row, tracked through its full lifecycle

        read = client.get(f"/tasks/{task_id}")  # => co-14: reads are open, no token needed
        assert read.status_code == 200  # => co-14: the just-created row is genuinely readable
        assert read.json()["status"] == "todo"  # => co-15: confirms the schema's DEFAULT applied server-side

        updated = client.put(  # => co-02: PUT replaces the full resource, guarded by require_token
            f"/tasks/{task_id}",
            json={"title": "write the report", "status": "done"},
            headers=AUTH,  # => co-02: full body
        )  # => co-18: valid token required for this write
        assert updated.status_code == 200  # => co-02: a successful replace on an existing id
        assert updated.json()["status"] == "done"  # => co-14: confirms the UPDATE actually landed

        deleted = client.delete(f"/tasks/{task_id}", headers=AUTH)  # => co-18: DELETE is guarded too
        assert deleted.status_code == 204  # => co-03: no body on a successful delete

        gone = client.get(f"/tasks/{task_id}")  # => co-14: re-reads the SAME id after deletion
        assert gone.status_code == 404  # => co-14: genuinely removed
        # => proves delete_task's cursor.rowcount check actually removed the row, not just returned 204

    def test_update_missing_id_is_404(self, client: TestClient) -> None:  # => co-02: PUT never creates
        response = client.put(  # => co-02: id 99999 was never created by this test
            "/tasks/99999",
            json={"title": "x", "status": "todo"},
            headers=AUTH,  # => co-18: a valid token is supplied
        )  # => co-18: a valid token alone does not manufacture a matching row
        assert response.status_code == 404  # => co-02: confirms PUT only replaces, never upserts
        # => distinguishes THIS 404 (valid token, missing row) from the 401 cases in TestTokenAuth below


# -- Token auth group (co-18) ------------------------------------------------------------
class TestTokenAuth:  # => co-18: isolates every auth-specific assertion under one namespace
    def test_missing_token_is_401(self, client: TestClient) -> None:  # => co-18: no header at all
        assert client.post("/tasks", json={"title": "a"}).status_code == 401  # => co-18: rejected before create_task runs
        # => credentials is None here -- the FIRST branch of require_token's "either failure mode" check

    def test_wrong_token_is_401(self, client: TestClient) -> None:  # => co-18: a header that fails the comparison
        response = client.post("/tasks", json={"title": "a"}, headers=BAD_AUTH)  # => co-18: wrong bearer value
        assert response.status_code == 401  # => co-18: require_token rejects a non-matching token too
        # => credentials.credentials != VALID_TOKEN here -- the SECOND branch of that same check

    def test_valid_token_succeeds(self, client: TestClient) -> None:  # => co-18: the "allowed" outcome
        response = client.post("/tasks", json={"title": "a"}, headers=AUTH)  # => co-18: exact VALID_TOKEN match
        assert response.status_code == 201  # => co-18: require_token returns None -- the write proceeds
        # => this is the ONE outcome where require_token does not raise at all

    def test_delete_also_requires_a_token(self, client: TestClient) -> None:  # => co-18: guard applies to every WRITE
        created = client.post("/tasks", json={"title": "b"}, headers=AUTH).json()  # => co-18: create needs a token too
        response = client.delete(f"/tasks/{created['id']}")  # => no Authorization header
        assert response.status_code == 401  # => co-18: DELETE is guarded exactly like POST and PUT
        # => confirms require_token is wired to remove_task too, not just post_task and put_task


# -- Pagination group (co-19) -------------------------------------------------------------
class TestPagination:  # => co-19: isolates every pagination/filter assertion under one namespace
    def test_seeded_pages_have_the_expected_window(self, client: TestClient) -> None:  # => co-19: bounded pages
        for i in range(20):  # => seeds 20 fresh tasks specifically for this pagination check
            client.post("/tasks", json={"title": f"paginated task {i}"}, headers=AUTH)  # => co-18: each needs a token
        first_page = client.get("/tasks", params={"limit": 5, "offset": 0})  # => co-19: no token needed for reads
        assert len(first_page.json()["items"]) == 5  # => co-19: a genuinely bounded page
        assert first_page.json()["next"] == 5  # => co-19: metadata points at the next window
        # => next == limit here because offset started at 0 -- the SAME next_offset formula app.py uses

    def test_status_filter_narrows_the_page(self, client: TestClient) -> None:  # => co-20: filter + pagination together
        created = client.post("/tasks", json={"title": "filter-target"}, headers=AUTH).json()  # => co-18: needs a token
        client.put(  # => co-20: sets status to "done" so the filter below has a real match to find
            f"/tasks/{created['id']}",  # => co-14: the path identifies WHICH row to update
            json={"title": "filter-target", "status": "done"},  # => co-02: PUT's full-replacement body
            headers=AUTH,  # => co-18: this write also needs a valid token
        )  # => co-18: PUT is a write, so a valid token is required here too
        response = client.get("/tasks", params={"status": "done", "limit": 50})  # => co-20: filtered read, no token
        body = response.json()  # => co-19, co-20: the SAME Page envelope shape as the standalone example
        assert all(t["status"] == "done" for t in body["items"])  # => co-20: every returned row matches
        # => a wide limit=50 with no offset ensures the filtered row above is genuinely inside this page


def test_full_integration_smoke_all_three_areas_together() -> None:  # => co-14, co-18, co-19: all three at once
    # => co-14, co-18, co-19: ONE test touching create (auth), read, list (pagination), and delete --
    # => the fullest single-test demonstration this example is named for
    client = TestClient(app)  # => co-22: a client built directly, outside the shared fixture above
    ids = [  # => co-14: creates 3 fresh tasks, each guarded by a valid token
        client.post("/tasks", json={"title": f"smoke {i}"}, headers=AUTH).json()["id"]  # => co-18: token required
        for i in range(3)  # => co-14: exactly 3 rows, enough to prove "list" without a large fixture
    ]  # => co-14: the 3 server-assigned ids, collected via a list comprehension
    listing = client.get("/tasks", params={"limit": 50})  # => co-19: an unguarded read, wide enough to see all 3
    assert all(any(t["id"] == i for t in listing.json()["items"]) for i in ids)  # => all 3 are listed
    # => co-19: proves list_page's SELECT genuinely returns rows this test itself just created
    for task_id in ids:  # => co-14: cleans up every id this test created, one DELETE per id
        assert client.delete(f"/tasks/{task_id}", headers=AUTH).status_code == 204  # => co-18: needs a token
    assert client.get(f"/tasks/{ids[0]}").status_code == 404  # => co-14: genuinely cleaned up
    # => spot-checks only the FIRST id -- the loop above already proved every delete call succeeded
