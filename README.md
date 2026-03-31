# Automated Reporting Pipeline

Un script en python para automatizar el reporte de ventas de retail. 

## qué hace

* limpia y prepara los datos de ventas del csv
* calcula facturación total, ticket medio, crecimiento mensual y descuento medio
* identifica los productos, tiendas y categorías con mejor rendimiento
* saca 4 gráficos automáticos para el reporte
* exporta un excel con 6 pestañas a `outputs/`

## estructura

```
automated-reporting-pipeline/
├── run.py             # script principal: ejecuta el flujo completo
├── pipeline.py        # procesamiento de datos y métricas
├── generate_data.py   # crea un csv de ventas sintético para probar
└── requirements.txt
```

## cómo ejecutarlo

```bash
pip install -r requirements.txt
python run.py
```

si no existe `data/sales.csv` se genera automáticamente al ejecutar.

## kpis que calcula

* facturación total y por periodo
* ticket medio por transacción
* crecimiento mes a mes (mom)
* descuento medio aplicado
* ranking de tiendas, productos y categorías

## stack

python · pandas · numpy · matplotlib · openpyxl
