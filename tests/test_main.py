from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_sheep():
    response = client.get("/sheep/1")

    assert response.status_code == 200
    assert response.json() == {

        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe"
    }

def test_add_sheep():
    new_sheep_data = {
        "id": 7,
        "name": "Margit",
        "breed": "Suffolk",
        "sex": "ewe"
    }

    response = client.post("/sheep", json=new_sheep_data)
    assert response.status_code == 201
    assert response.json() == new_sheep_data
    get_response = client.get(f"/sheep/{new_sheep_data['id']}")
    assert get_response.status_code == 200

def test_delete_sheep():
    sheep_data = {
        "id": 8,
        "name": "Bobby",
        "breed": "Gotland",
        "sex": "ram"
    }
    client.post("/sheep", json=sheep_data)

    response = client.delete(f"/sheep/{sheep_data['id']}")
    assert response.status_code == 204

    get_response = client.delete(f"/sheep/{sheep_data['id']}")
    assert get_response.status_code == 404


def test_update_sheep():
    sheep_data = {
        "id": 9,
        "name": "Luna",
        "breed": "Gotland",
        "sex": "ewe"
    }
    client.post("/sheep", json=sheep_data)

    updated_data = {
        "id": 9,
        "name": "Luna",
        "breed": "Gotland",
        "sex": "ewe"
    }
    response = client.put(f"/sheep/{sheep_data['id']}", json=updated_data)
    assert response.status_code == 200
    assert response.json() == updated_data

    get_response = client.get(f"/sheep/{updated_data['id']}")
    assert get_response.status_code == 200
    assert get_response.json() == updated_data


def test_read_all_sheep():
    client.post("/sheep", json={"id": 10, "name": "Max", "breed": "Suffolk", "sex": "ram"})
    client.post("/sheep", json={"id": 11, "name": "Bella", "breed": "Suffolk", "sex": "ewe"})

    response = client.get("/sheep")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 2