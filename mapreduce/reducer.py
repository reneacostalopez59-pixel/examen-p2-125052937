#!/usr/bin/env python3
import sys

acumulado = {}

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        producto, ingreso_str = line.split("\t", 1)
        ingreso = float(ingreso_str)
        acumulado[producto] = acumulado.get(producto, 0.0) + ingreso
    except ValueError:
        continue

# Ordenar de mayor a menor ingreso total y tomar el Top 10
top_10 = sorted(acumulado.items(), key=lambda x: x[1], reverse=True)[:10]

for producto, total in top_10:
    print(f"{producto}\t{total:.2f}")