#!/usr/bin/env python3
import sys
import csv

IDX_PRODUCTO = 4
IDX_CANTIDAD = 5
IDX_PRECIO = 6

archivo_csv = sys.argv[1] if len(sys.argv) > 1 else "/data/input/ventas_125052937.csv"
acumulado = {}

with open(archivo_csv, mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        try:
            if not row or len(row) <= max(IDX_PRODUCTO, IDX_CANTIDAD, IDX_PRECIO):
                continue
            if row[IDX_CANTIDAD].strip().lower() == "cantidad":
                continue

            producto = row[IDX_PRODUCTO].strip()
            cantidad = float(row[IDX_CANTIDAD])
            precio_unitario = float(row[IDX_PRECIO])

            if not producto:
                continue

            acumulado[producto] = acumulado.get(producto, 0.0) + (cantidad * precio_unitario)
        except (ValueError, IndexError):
            continue

top_10 = sorted(acumulado.items(), key=lambda x: x[1], reverse=True)[:10]

for producto, total in top_10:
    print(f"{producto}\t{total:.2f}")
