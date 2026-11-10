import os
import time
import psycopg2  # type: ignore[reportMissingModuleSource]
from psycopg2.extras import RealDictCursor  # type: ignore[reportMissingModuleSource]
from flask import Flask, jsonify, request

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        user=os.getenv("POSTGRES_USER", "admin"),
        password=os.getenv("POSTGRES_PASSWORD", "admin123"),
        dbname=os.getenv("POSTGRES_DB", "datamart")
    )

def init_db():
    for _ in range(10):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS resultados (
                        clave VARCHAR(150) PRIMARY KEY,
                        ingreso_total NUMERIC(15, 2) NOT NULL
                    );
                """)
                conn.commit()
            conn.close()
            break
        except Exception:
            time.sleep(2)

@app.route("/resultados", methods=["GET"])
def obtener_resultados():
    conn = get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT clave AS producto, ingreso_total FROM resultados ORDER BY ingreso_total DESC;")
        filas = cur.fetchall()
    conn.close()
    return jsonify(filas), 200

@app.route("/resultados/<clave>", methods=["GET"])
def obtener_por_clave(clave):
    conn = get_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT clave AS producto, ingreso_total FROM resultados WHERE clave = %s;", (clave,))
        fila = cur.fetchone()
    conn.close()
    if not fila:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify(fila), 200

@app.route("/resultados", methods=["POST"])
def crear_o_actualizar_resultado():
    data = request.get_json()
    if not data or "producto" not in data or "ingreso_total" not in data:
        return jsonify({"error": "Se requieren 'producto' e 'ingreso_total'"}), 400
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO resultados (clave, ingreso_total)
            VALUES (%s, %s)
            ON CONFLICT (clave) DO UPDATE SET ingreso_total = EXCLUDED.ingreso_total;
        """, (data["producto"], float(data["ingreso_total"])))
        conn.commit()
    conn.close()
    return jsonify({"mensaje": "Registro guardado exitosamente", "producto": data["producto"]}), 201

@app.route("/resultados/<clave>", methods=["DELETE"])
def eliminar_resultado(clave):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM resultados WHERE clave = %s;", (clave,))
        eliminados = cur.rowcount
        conn.commit()
    conn.close()
    if eliminados == 0:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify({"mensaje": f"Producto '{clave}' eliminado"}), 200

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8000)