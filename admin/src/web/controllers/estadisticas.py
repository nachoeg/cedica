from flask import Blueprint, render_template, url_for, send_file
import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt
import io
from datetime import datetime
from src.core.database import db
from src.core.cobros.cobro import Cobro
from src.core.cobros import obtener_ingresos_por_mes

bp = Blueprint("estadisticas", __name__, url_prefix="/estadisticas")


@bp.get("/")
def index():
    return reporte_propuestas_trabajo()


@bp.get("/grafico_ingresos")
def grafico_ingresos():
    return render_template(
        "pages/estadisticas/ver_grafico.html",
        titulo="Gráfico de ingresos",
        imagen_url=url_for("estadisticas.grafico_ingresos_imagen"),
    )


@bp.get("/grafico_ingresos/grafico")
def grafico_ingresos_imagen():
    # Obtener los datos de los cobros desde la base de datos
    cobros = obtener_ingresos_por_mes()

    # Extraer las fechas y los montos de los cobros
    fechas = [cobro.fecha_pago for cobro in cobros]
    montos = [cobro.monto for cobro in cobros]

    # Crear el gráfico
    plt.figure(figsize=(10, 5))
    plt.plot(fechas, montos, marker="o", linestyle="-", label="Montos de ingresos")

    # Agregar etiquetas y título
    plt.xlabel("Fecha de Pago")
    plt.ylabel("Monto")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Mostrar leyenda
    plt.legend()

    # Guardar el gráfico en un objeto BytesIO
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plt.close()

    return send_file(img, mimetype="image/png")


@bp.get("/grafico_discapacidades")
def grafico_discapacidades():
    return render_template(
        "pages/estadisticas/ver_grafico.html",
        titulo="Gráfico de tipos de discapacidad",
        imagen_url=url_for("estadisticas.grafico_discapacidades_imagen"),
    )


@bp.get("/grafico_discapacidades/grafico")
def grafico_discapacidades_imagen():
    # Obtener los datos de los cobros desde la base de datos
    cobros = obtener_ingresos_por_mes()

    # Extraer las fechas y los montos de los cobros
    fechas = [cobro.fecha_pago for cobro in cobros]
    montos = [cobro.monto for cobro in cobros]

    # Crear el gráfico
    plt.figure(figsize=(10, 5))
    plt.plot(fechas, montos, marker="o", linestyle="-", label="Montos de ingresos")

    # Agregar etiquetas y título
    plt.xlabel("Fecha de Pago")
    plt.ylabel("Monto")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Mostrar leyenda
    plt.legend()

    # Guardar el gráfico en un objeto BytesIO
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plt.close()

    return send_file(img, mimetype="image/png")


@bp.get("/reporte_propuestas_trabajo")
def reporte_propuestas_trabajo():
    return render_template(
        "pages/estadisticas/ver_reporte.html",
        titulo="Reporte de propuestas de trabajo",
    )
