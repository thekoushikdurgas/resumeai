"""API smoke tests."""

import json
import os

import pytest
from fastapi.testclient import TestClient

from app.clients import s3storage_client
from app.main import app

API_KEY = os.environ["API_KEY"]
HEADERS = {"X-API-Key": API_KEY}


@pytest.fixture(autouse=True)
def mock_s3storage(monkeypatch: pytest.MonkeyPatch):
    """In-memory fake s3storage so tests do not call AWS/API Gateway."""
    s3storage_client.get_s3storage_client.cache_clear()
    store: dict[tuple[str, str], dict] = {}

    class FakeStorage:
        async def upload_resume_json(self, bucket_id: str, filename: str, data: bytes) -> str:
            key = f"resume/{filename}"
            store[(bucket_id, key)] = json.loads(data.decode("utf-8"))
            return key

        async def fetch_json_object(self, bucket_id: str, file_key: str) -> dict:
            return dict(store[(bucket_id, file_key)])

        async def delete_file(self, bucket_id: str, file_key: str) -> None:
            store.pop((bucket_id, file_key), None)

    fake = FakeStorage()
    monkeypatch.setattr(
        "app.services.resume_service.get_s3storage_client",
        lambda: fake,
    )
    yield
    s3storage_client.get_s3storage_client.cache_clear()


@pytest.fixture
def client():
    # Lifespan runs init_db (create tables) — required for CRUD tests
    with TestClient(app) as c:
        yield c


def test_root(client: TestClient):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "running"


def test_health(client: TestClient):
    r = client.get("/v1/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_health_info(client: TestClient):
    r = client.get("/v1/health/info")
    assert r.status_code == 200
    assert "version" in r.json()


def test_resume_crud(client: TestClient):
    from app.models.resume import PersonalDetails, Resume

    minimal = Resume(
        personalDetails=PersonalDetails(
            name="Test User",
            title="Engineer",
            email="a@b.com",
            phone="1",
            location="Earth",
        ),
        objective="Do things",
    )
    payload = {"resume": minimal.model_dump(mode="json"), "userId": "user-1"}
    r = client.post("/v1/resume", json=payload, headers=HEADERS)
    assert r.status_code == 201, r.text
    rid = r.json()["id"]
    g = client.get(f"/v1/resume/{rid}", headers=HEADERS)
    assert g.status_code == 200
    assert g.json()["userId"] == "user-1"
    lst = client.get("/v1/resume/user/user-1", headers=HEADERS)
    assert lst.status_code == 200
    assert len(lst.json()) >= 1
    d = client.delete(f"/v1/resume/{rid}", headers=HEADERS)
    assert d.status_code == 204


def test_unauthorized_without_key(client: TestClient):
    r = client.get("/v1/resume/user/x")
    assert r.status_code == 422  # missing header
