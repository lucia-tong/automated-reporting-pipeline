# procesamiento de datos y generación de métricas

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

COLORES = ["#1C2F5E", "#2C7BB6", "#4DAC26", "#F4A235", "#D7191C"]


def cargar_datos():
    print("Cargando datos...")
    df = pd.read_csv("data/sales.csv", parse_dates=["fecha"])
    print(f"  {len(df):,} transacciones cargadas")
    return df


def transformar(df):
    df = df.copy()
    df["mes"]     = df["fecha"].dt.to_period("M").dt.to_timestamp()
    df["semana"]  = df["fecha"].dt.to_period("W").dt.start_time
    df["dia_sem"] = df["fecha"].dt.day_name()
    return df


def resumen_general(df):
    total      = df["total"].sum()
    num_ventas = len(df)
    ticket_med = df["total"].mean()
    unidades   = df["cantidad"].sum()
    desc_medio = df["descuento"].mean()
    top_prod   = df.groupby("producto")["total"].sum().idxmax()
    top_tienda = df.groupby("tienda")["total"].sum().idxmax()
    top_cat    = df.groupby("categoria")["total"].sum().idxmax()

    return {
        "Facturación total":  f"${total:,.0f}",
        "Nº transacciones":   f"{num_ventas:,}",
        "Unidades vendidas":  f"{unidades:,}",
        "Ticket medio":       f"${ticket_med:.2f}",
        "Descuento medio":    f"{desc_medio:.1%}",
        "Producto top":       top_prod,
        "Tienda top":         top_tienda,
        "Categoría top":      top_cat,
    }


def ventas_mensuales(df):
    agg = df.groupby("mes").agg(
        facturacion  =("total",    "sum"),
        transacciones=("total",    "count"),
        unidades     =("cantidad", "sum"),
    ).reset_index()
    agg["ticket_medio"] = (agg["facturacion"] / agg["transacciones"]).round(2)
    # crecimiento mes a mes
    agg["crecimiento_mom"] = agg["facturacion"].pct_change().round(4)
    return agg


def ventas_por_tienda(df):
    return df.groupby("tienda").agg(
        facturacion  =("total",    "sum"),
        transacciones=("total",    "count"),
        ticket_medio =("total",    "mean"),
    ).reset_index().sort_values("facturacion", ascending=False).round(2)


def ventas_por_categoria(df):
    agg = df.groupby("categoria").agg(
        facturacion  =("total",    "sum"),
        unidades     =("cantidad", "sum"),
    ).reset_index()
    agg["pct"] = (agg["facturacion"] / agg["facturacion"].sum()).round(4)
    return agg.sort_values("facturacion", ascending=False)


def top_productos(df):
    return df.groupby("producto").agg(
        facturacion  =("total",     "sum"),
        unidades     =("cantidad",  "sum"),
        desc_medio   =("descuento", "mean"),
    ).reset_index().sort_values("facturacion", ascending=False).round(2)


def grafico_mensual(mensual):
    fig, ax1 = plt.subplots(figsize=(10, 4))
    ax2 = ax1.twinx()
    meses = mensual["mes"].dt.strftime("%b %Y")
    x = range(len(meses))
    ax1.bar(x, mensual["facturacion"], color=COLORES[0], alpha=0.75, label="Facturación")
    ax2.plot(x, mensual["crecimiento_mom"] * 100, color=COLORES[3],
             marker="o", linewidth=2, markersize=5, label="Crecimiento MoM %")
    ax2.axhline(0, color=COLORES[4], linewidth=0.8, linestyle="--")
    ax1.set_xticks(x)
    ax1.set_xticklabels(meses, rotation=30, ha="right")
    ax1.set_ylabel("Facturación (USD)", color=COLORES[0])
    ax2.set_ylabel("Crecimiento MoM %", color=COLORES[3])
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax1.set_title("Facturación mensual y crecimiento", fontweight="bold")
    ax1.spines[["top", "right"]].set_visible(False)
    lineas = [plt.Rectangle((0,0),1,1, color=COLORES[0], alpha=0.75),
              plt.Line2D([0],[0], color=COLORES[3], marker="o")]
    ax1.legend(lineas, ["Facturación", "Crecimiento MoM %"], loc="upper left", fontsize=9)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "facturacion_mensual.png", dpi=150)
    plt.close()
    print("  Gráfico guardado: facturacion_mensual.png")


def grafico_tiendas(tiendas):
    fig, ax = plt.subplots(figsize=(8, 4))
    colores = [COLORES[i % len(COLORES)] for i in range(len(tiendas))]
    barras  = ax.barh(tiendas["tienda"], tiendas["facturacion"], color=colores)
    ax.bar_label(barras, fmt="$%.0f", padding=4, fontsize=9)
    ax.set_xlabel("Facturación total (USD)")
    ax.set_title("Facturación por tienda", fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "ventas_tiendas.png", dpi=150)
    plt.close()
    print("  Gráfico guardado: ventas_tiendas.png")


def grafico_categorias(categorias):
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.pie(
        categorias["facturacion"],
        labels=categorias["categoria"],
        colors=COLORES[:len(categorias)],
        autopct="%1.1f%%",
        startangle=140,
        wedgeprops={"linewidth": 1.5, "edgecolor": "white"}
    )
    ax.set_title("Facturación por categoría", fontweight="bold")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "categorias.png", dpi=150)
    plt.close()
    print("  Gráfico guardado: categorias.png")


def grafico_dia_semana(df):
    orden = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    etiquetas = ["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"]
    agg = df.groupby("dia_sem")["total"].sum().reindex(orden)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(etiquetas, agg.values, color=COLORES[1], alpha=0.8)
    ax.set_ylabel("Facturación (USD)")
    ax.set_title("Facturación por día de la semana", fontweight="bold")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v:,.0f}"))
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "dias_semana.png", dpi=150)
    plt.close()
    print("  Gráfico guardado: dias_semana.png")


def exportar_excel(kpis, mensual, tiendas, categorias, productos, df):
    path = OUTPUT_DIR / "reporte_ventas.xlsx"
    kpi_df = pd.DataFrame(list(kpis.items()), columns=["Métrica", "Valor"])
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        kpi_df.to_excel(writer,    sheet_name="KPIs",         index=False)
        mensual.to_excel(writer,   sheet_name="Ventas mensuales", index=False)
        tiendas.to_excel(writer,   sheet_name="Por tienda",    index=False)
        categorias.to_excel(writer,sheet_name="Por categoría", index=False)
        productos.to_excel(writer, sheet_name="Productos",     index=False)
        df.to_excel(writer,        sheet_name="Datos raw",     index=False)
    print(f"  Excel exportado → {path}")


def main():
    print(f"\nAutomated Reporting Pipeline — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    df        = cargar_datos()
    df        = transformar(df)

    print("Calculando métricas...")
    kpis      = resumen_general(df)
    mensual   = ventas_mensuales(df)
    tiendas   = ventas_por_tienda(df)
    categorias= ventas_por_categoria(df)
    productos = top_productos(df)

    print("\nResumen de negocio:")
    for k, v in kpis.items():
        print(f"  {k:<22} {v}")

    print("\nGenerando gráficos...")
    grafico_mensual(mensual)
    grafico_tiendas(tiendas)
    grafico_categorias(categorias)
    grafico_dia_semana(df)

    print("\nExportando Excel...")
    exportar_excel(kpis, mensual, tiendas, categorias, productos, df)

    print("\nTodo listo. Resultados en outputs/\n")


if __name__ == "__main__":
    main()
