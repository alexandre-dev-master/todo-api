from fastapi.testclient import TestClient


def test_create_task(client: TestClient, auth_token: str):
    response = client.post(
        "/tasks/",
        json={"title": "My first task", "description": "API test"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 201

    data = response.json()

    assert data["success"] is True
    assert data["data"]["title"] == "My first task"


def test_get_tasks(client: TestClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}

    client.post(
        "/tasks/",
        json={"title": "Task 1", "description": "First task"},
        headers=headers,
    )

    client.post(
        "/tasks/",
        json={"title": "Task 2", "description": "Second task"},
        headers=headers,
    )

    response = client.get("/tasks/", headers=headers)

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert len(data["data"]) == 2


def test_update_task(client: TestClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}

    create_response = client.post(
        "/tasks/",
        json={"title": "Old task", "description": "Old description"},
        headers=headers,
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["data"]["id"]

    response = client.put(
        f"/tasks/{task_id}", json={"title": "Updated task"}, headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["data"]["title"] == "Updated task"


def test_delete_task(client: TestClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}

    create_response = client.post(
        "/tasks/",
        json={"title": "Task to delete", "description": "Will be removed"},
        headers=headers,
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["data"]["id"]

    response = client.delete(f"/tasks/{task_id}", headers=headers)

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["data"] is None

    list_response = client.get("/tasks/", headers=headers)

    tasks = list_response.json()["data"]

    assert len(tasks) == 0


def test_user_cannot_update_other_user_task(client: TestClient, create_user_token):
    token_user_a = create_user_token("user_a@example.com")
    token_user_b = create_user_token("user_b@example.com")

    headers_a = {"Authorization": f"Bearer {token_user_a}"}

    headers_b = {"Authorization": f"Bearer {token_user_b}"}

    create_response = client.post(
        "/tasks/",
        json={"title": "User A task", "description": "Private task"},
        headers=headers_a,
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["data"]["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "Unauthorized update attempt"},
        headers=headers_b,
    )

    assert response.status_code == 403

    data = response.json()

    assert data["detail"] == ("You do not have permission to update this task.")


def test_user_cannot_delete_other_user_task(client: TestClient, create_user_token):
    token_user_a = create_user_token("delete_a@example.com")
    token_user_b = create_user_token("delete_b@example.com")

    headers_a = {"Authorization": f"Bearer {token_user_a}"}

    headers_b = {"Authorization": f"Bearer {token_user_b}"}

    create_response = client.post(
        "/tasks/",
        json={"title": "Protected task", "description": "Should not be deleted"},
        headers=headers_a,
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["data"]["id"]

    response = client.delete(f"/tasks/{task_id}", headers=headers_b)

    assert response.status_code == 403

    data = response.json()

    assert data["detail"] == ("You do not have permission to delete this task.")
