import os
import psycopg2

RUTA_SALIDA = "/data/output/resultado/part-00000"

def cargar():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        user=os.getenv("POSTGRES_USER", "admin"),
        password=os.getenv("POSTGRES_PASSWORD", "admin123"),
        dbname=os.getenv("POSTGRES_DB", "datamart")
    )
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS resultados (
                clave VARCHAR(150) PRIMARY KEY,
                ingreso_total NUMERIC(15, 2) NOT NULL
            );
        """)
        with open(RUTA_SALIDA, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                producto, ingreso = linea.split("\t", 1)
                cur.execute("""
                    INSERT INTO resultados (clave, ingreso_total)
                    VALUES (%s, %s)
                    ON CONFLICT (clave) DO UPDATE SET ingreso_total = EXCLUDED.ingreso_total;
                """, (producto, float(ingreso)))
        conn.commit()
    conn.close()
    print("Resultados cargados correctamente en PostgreSQL.")

if __name__ == "__main__":
    cargar()