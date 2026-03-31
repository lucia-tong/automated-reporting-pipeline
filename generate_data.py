# genera datos sintéticos de ventas retail para probar el pipeline

import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(99)

PRODUCTOS = [
    {"nombre": "Camiseta Básica",    "categoria": "Ropa",        "precio": 19.99},
    {"nombre": "Pantalón Vaquero",   "categoria": "Ropa",        "precio": 49.99},
    {"nombre": "Zapatillas Running", "categoria": "Calzado",     "precio": 89.99},
    {"nombre": "Mochila Urbana",     "categoria": "Accesorios",  "precio": 35.00},
    {"nombre": "Gorra Logo",         "categoria": "Accesorios",  "precio": 14.99},
    {"nombre": "Chaqueta Impermeable","categoria": "Ropa",       "precio": 79.99},
    {"nombre": "Calcetines Pack 3",  "categoria": "Ropa",        "precio": 9.99},
    {"nombre": "Cinturón Cuero",     "categoria": "Accesorios",  "precio": 24.99},
]

TIENDAS = ["Madrid Centro", "Barcelona Gràcia", "Valencia Nord",
           "Sevilla Triana", "Online"]

FECHAS = pd.date_range("2024-01-01", "2024-06-30", freq="D")

filas = []
for fecha in FECHAS:
    # más ventas los fines de semana
    n = np.random.poisson(18 if fecha.weekday() >= 5 else 11)
    for _ in range(n):
        producto = PRODUCTOS[np.random.randint(len(PRODUCTOS))]
        tienda   = TIENDAS[np.random.randint(len(TIENDAS))]
        cantidad = np.random.choice([1, 2, 3], p=[0.70, 0.22, 0.08])
        descuento = np.random.choice([0, 0.05, 0.10, 0.20], p=[0.55, 0.20, 0.15, 0.10])
        total    = round(producto["precio"] * cantidad * (1 - descuento), 2)

        filas.append({
            "fecha":     fecha.strftime("%Y-%m-%d"),
            "producto":  producto["nombre"],
            "categoria": producto["categoria"],
            "tienda":    tienda,
            "cantidad":  cantidad,
            "precio_unit": producto["precio"],
            "descuento": descuento,
            "total":     total,
        })

Path("data").mkdir(exist_ok=True)
df = pd.DataFrame(filas)
df.to_csv("data/sales.csv", index=False)
print(f"CSV generado: {len(df)} transacciones → data/sales.csv")
