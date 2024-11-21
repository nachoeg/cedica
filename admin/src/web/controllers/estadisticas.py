from flask import Blueprint, render_template, url_for, send_file, redirect
import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt
import io
from datetime import datetime
from src.core.database import db
from src.core.cobros.cobro import Cobro
from src.core.cobros import obtener_ingresos_por_mes
from src.core.jinetes_y_amazonas import obtener_ranking_propuestas, obtener_cant_tipos_discapacidad, obtener_tipos_discapacidad

bp = Blueprint("estadisticas", __name__, url_prefix="/estadisticas")


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
    tipos_discapacidad = obtener_tipos_discapacidad()

    tipos_discapacidad_cant = obtener_cant_tipos_discapacidad()
    tipos_discapacidad_cant.sort(key=lambda x: x[0])

    total = 0

    lista = [{"id": tipo[0],
              "nombre": tipo[1],
              "cant": 0} for tipo in tipos_discapacidad]

    for item in tipos_discapacidad_cant:
        id = item[0] - 1
        lista[id]["cant"] = item[1]
        total += item[1]

    leyendas = [tipo_disc[1] for tipo_disc in tipos_discapacidad]
    porcentajes = [x["cant"]*100/total for x in lista]

    fig, ax = plt.subplots()
    ax.pie(porcentajes, labels=leyendas, autopct='%1.1f%%')

    # Guardar el gráfico en un objeto BytesIO
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plt.close()

    return send_file(img, mimetype="image/png")


@bp.get("/reporte_propuestas_trabajo")
def reporte_propuestas_trabajo():
    resultados_actuales, resultados_historicos = obtener_ranking_propuestas()
    ranking_actuales_con_puestos = []
    ranking_historico_con_puestos = []
    for indice, item in enumerate(resultados_actuales, start=1):
        ranking_actuales_con_puestos.append(({"puesto": indice,
                                              "propuesta": item[0],
                                              "cantidad": item[1]}))

    for indice, item in enumerate(resultados_historicos, start=1):
        ranking_historico_con_puestos.append(({"puesto": indice,
                                               "propuesta": item[0],
                                               "cantidad": item[1]}))
    return render_template(
        "pages/estadisticas/ver_ranking_propuestas.html",
        ranking_actual=ranking_actuales_con_puestos,
        ranking_historico=ranking_historico_con_puestos,
        titulo="Reporte de propuestas de trabajo",
    )
