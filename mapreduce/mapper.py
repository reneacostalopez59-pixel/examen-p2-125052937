#!/usr/bin/env python3
import sys
import csv

# Ajusta estos índices (empezando en 0) según el orden de columnas de tu CSV:
IDX_PRODUCTO = 4
IDX_CANTIDAD = 5
IDX_PRECIO = 6

reader = csv.reader(sys.stdin)

for row in reader:
    try:
        if not row or len(row) <= max(IDX_PRODUCTO, IDX_CANTIDAD, IDX_PRECIO):
            continue
        # Ignorar el encabezado del CSV
        if row[IDX_CANTIDAD].strip().lower() == "cantidad" or row[IDX_PRECIO].strip().lower() == "precio_unitario":
            continue

        producto = row[IDX_PRODUCTO].strip()
        cantidad = float(row[IDX_CANTIDAD])
        precio_unitario = float(row[IDX_PRECIO])

        if not producto:
            continue

        ingreso = cantidad * precio_unitario
        print(f"{producto}\t{ingreso}")
    except (ValueError, IndexError):
        # Ignorar líneas mal formadas sin truncar el job
        continue