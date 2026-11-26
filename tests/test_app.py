import pytest

from app import create_app, validar


@pytest.fixture
def client(tmp_path):
    app = create_app(str(tmp_path / "test.db"))
    app.config["TESTING"] = True
    return app.test_client()


def nueva(client, **extra):
    datos = {"nombre": "Realizar actividad DevOps", "descripcion": "Entrega", "prioridad": "Alta"}
    datos.update(extra)
    return client.post("/api/tareas", json=datos)


def test_registro_tarea(client):  # CP01 / RF01
    r = nueva(client)
    assert r.status_code == 201
    assert r.get_json()["nombre"] == "Realizar actividad DevOps"
    assert r.get_json()["estado"] == "Pendiente"


def test_registro_sin_nombre(client):  # CP02
    r = nueva(client, nombre="  ")
    assert r.status_code == 400
    assert "obligatorio" in r.get_json()["error"]


def test_consultar_tareas(client):  # CP03 / RF02
    nueva(client)
    nueva(client, nombre="Otra tarea")
    r = client.get("/api/tareas")
    assert r.status_code == 200
    assert len(r.get_json()) == 2


def test_editar_tarea(client):  # CP04 / RF03
    id_ = nueva(client).get_json()["id"]
    r = client.put(f"/api/tareas/{id_}", json={"nombre": "Editada", "prioridad": "Baja"})
    assert r.status_code == 200
    assert r.get_json()["nombre"] == "Editada"
    assert r.get_json()["prioridad"] == "Baja"


def test_eliminar_tarea(client):  # CP05 / RF04
    id_ = nueva(client).get_json()["id"]
    assert client.delete(f"/api/tareas/{id_}").status_code == 200
    assert client.get("/api/tareas").get_json() == []


def test_cambiar_estado(client):  # CP06 / RF05
    id_ = nueva(client).get_json()["id"]
    r = client.patch(f"/api/tareas/{id_}/estado", json={"estado": "En proceso"})
    assert r.get_json()["estado"] == "En proceso"
    r = client.patch(f"/api/tareas/{id_}/estado", json={"estado": "Inventado"})
    assert r.status_code == 400


def test_prioridad(client):  # CP07 / RF06
    assert nueva(client, prioridad="Media").get_json()["prioridad"] == "Media"
    assert nueva(client, prioridad="Urgente").status_code == 400


def test_tarea_inexistente(client):
    assert client.delete("/api/tareas/999").status_code == 404
    assert client.put("/api/tareas/999", json={"nombre": "x"}).status_code == 404


def test_validar_datos_invalidos():
    datos, error = validar(None)
    assert datos is None and error
