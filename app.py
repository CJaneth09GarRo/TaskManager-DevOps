import os
import sqlite3

from flask import Flask, g, jsonify, render_template, request

ESTADOS = ["Pendiente", "En proceso", "Terminada"]
PRIORIDADES = ["Alta", "Media", "Baja"]


def validar(data, parcial=False):
    """Devuelve (datos_limpios, error)."""
    if not isinstance(data, dict):
        return None, "Datos inválidos."
    limpio = {}
    if not parcial or "nombre" in data:
        nombre = str(data.get("nombre", "")).strip()
        if not nombre:
            return None, "El nombre de la tarea es obligatorio."
        limpio["nombre"] = nombre
    if not parcial or "descripcion" in data:
        limpio["descripcion"] = str(data.get("descripcion", "")).strip()
    if not parcial or "estado" in data:
        estado = data.get("estado", "Pendiente")
        if estado not in ESTADOS:
            return None, "Estado inválido. Usa: " + ", ".join(ESTADOS) + "."
        limpio["estado"] = estado
    if not parcial or "prioridad" in data:
        prioridad = data.get("prioridad", "Media")
        if prioridad not in PRIORIDADES:
            return None, "Prioridad inválida. Usa: " + ", ".join(PRIORIDADES) + "."
        limpio["prioridad"] = prioridad
    return limpio, None


def create_app(db_path=None):
    app = Flask(__name__)
    app.config["DATABASE"] = db_path or os.environ.get(
        "DATABASE", os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.db")
    )

    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row
        return g.db

    @app.teardown_appcontext
    def cerrar_db(_):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    with app.app_context():
        get_db().execute(
            """CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT DEFAULT '',
                estado TEXT NOT NULL DEFAULT 'Pendiente',
                prioridad TEXT NOT NULL DEFAULT 'Media'
            )"""
        )
        get_db().commit()

    def obtener(id_):
        fila = get_db().execute("SELECT * FROM tareas WHERE id = ?", (id_,)).fetchone()
        return dict(fila) if fila else None

    def no_existe():
        return jsonify({"error": "La tarea no existe."}), 404

    @app.get("/")
    def inicio():
        return render_template("index.html")

    @app.get("/api/tareas")  # RF02
    def listar():
        filas = get_db().execute("SELECT * FROM tareas ORDER BY id DESC").fetchall()
        return jsonify([dict(f) for f in filas])

    @app.post("/api/tareas")  # RF01 y RF06
    def crear():
        datos, error = validar(request.get_json(silent=True))
        if error:
            return jsonify({"error": error}), 400
        db = get_db()
        cur = db.execute(
            "INSERT INTO tareas (nombre, descripcion, estado, prioridad) VALUES (?, ?, ?, ?)",
            (datos["nombre"], datos["descripcion"], datos["estado"], datos["prioridad"]),
        )
        db.commit()
        return jsonify(obtener(cur.lastrowid)), 201

    @app.put("/api/tareas/<int:id_>")  # RF03
    def editar(id_):
        if not obtener(id_):
            return no_existe()
        datos, error = validar(request.get_json(silent=True))
        if error:
            return jsonify({"error": error}), 400
        db = get_db()
        db.execute(
            "UPDATE tareas SET nombre=?, descripcion=?, estado=?, prioridad=? WHERE id=?",
            (datos["nombre"], datos["descripcion"], datos["estado"], datos["prioridad"], id_),
        )
        db.commit()
        return jsonify(obtener(id_))

    @app.patch("/api/tareas/<int:id_>/estado")  # RF05
    def cambiar_estado(id_):
        if not obtener(id_):
            return no_existe()
        payload = request.get_json(silent=True) or {}
        datos, error = validar({"estado": payload.get("estado")}, parcial=True)
        if error:
            return jsonify({"error": error}), 400
        db = get_db()
        db.execute("UPDATE tareas SET estado=? WHERE id=?", (datos["estado"], id_))
        db.commit()
        return jsonify(obtener(id_))

    @app.delete("/api/tareas/<int:id_>")  # RF04
    def eliminar(id_):
        if not obtener(id_):
            return no_existe()
        db = get_db()
        db.execute("DELETE FROM tareas WHERE id=?", (id_,))
        db.commit()
        return jsonify({"mensaje": "Tarea eliminada."})

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
