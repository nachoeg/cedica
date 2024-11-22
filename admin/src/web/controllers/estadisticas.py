import io
import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt
from flask import Blueprint, render_template, url_for, send_file, redirect, request

from src.core.cobros import obtener_ingresos_por_mes
from src.core.jinetes_y_amazonas import (
    obtener_ranking_propuestas,
    obtener_cant_tipos_discapacidad,
    obtener_tipos_discapacidad,
    obtener_dia,
    obtener_ranking_jinetes_por_dia)
from src.core.jinetes_y_amazonas import obtener_cantidad_becados
from src.core.jinetes_y_amazonas import listar_deudores
from src.web.handlers.funciones_auxiliares import convertir_a_entero

bp = Blueprint("estadisticas", __name__, url_prefix="/estadisticas")


@bp.get("/")
def index():
    return redirect(url_for("estadisticas.reporte_propuestas_trabajo"))


@bp.get("/grafico_ingresos")
def grafico_ingresos():
    return render_template(
        "pages/estadisticas/ver_grafico.html",
        titulo="Gráfico de ingresos por mes",
        imagen_url=url_for("estadisticas.grafico_ingresos_imagen"),
    )


@bp.get("/grafico_ingresos/grafico")
def grafico_ingresos_imagen():
    # Obtener los datos de los cobros desde la base de datos
    ingresos_por_mes = obtener_ingresos_por_mes()

    # Extraer las fechas y los montos de los cobros
    fechas = [ingreso.mes.strftime("%Y-%m") for ingreso in reversed(ingresos_por_mes)]
    montos = [ingreso.total_ingresos for ingreso in reversed(ingresos_por_mes)]

    # Crear el gráfico de barras
    plt.figure(figsize=(10, 5))
    bars = plt.bar(fechas, montos, label="Montos de ingresos")

    # Agregar etiquetas y título
    plt.xlabel("Fecha de Pago")
    plt.ylabel("Monto")
    plt.title("Ingresos por Mes")
    plt.tight_layout()

    # Mostrar leyenda
    plt.legend()

    # Agregar etiquetas con los valores de los ingresos en cada barra
    for bar in bars:
        yval = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            yval,
            f"{yval:.2f}",
            ha="center",
            va="bottom",
        )

    # Guardar el gráfico en un objeto BytesIO
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plt.close()

    return send_file(img, mimetype="image/png")


@bp.get("/grafico_becados")
def grafico_becados():
    return render_template(
        "pages/estadisticas/ver_grafico.html",
        titulo="Gráfico de jinetes y amazonas becados",
        imagen_url=url_for("estadisticas.grafico_becados_imagen"),
    )


@bp.get("/grafico_becados/grafico")
def grafico_becados_imagen():
    # Obtener los datos de los J&A becados desde la base de datos
    total_becados, total_no_becados = obtener_cantidad_becados()

    # Verificar si hay datos
    if total_becados == 0 and total_no_becados == 0:
        # Crear una imagen alternativa indicando que no hay datos
        plt.figure(figsize=(6, 3))
        plt.text(
            0.5, 0.5, "No hay datos disponibles", ha="center", va="center", fontsize=12
        )
        plt.axis("off")
        
    else:
        # Crear el gráfico de tortas
        labels = [f"Becados ({total_becados})", f"No Becados ({total_no_becados})"]
        sizes = [total_becados, total_no_becados]
        colors = ["#ff9999", "#66b3ff"]

        def autopct_format(pct):
            # Mostrar el porcentaje solo si es mayor a 0
            return f"{pct:.1f}%" if pct > 0 else ""

        plt.figure(figsize=(6, 6))
        wedges, texts, autotexts = plt.pie(
            sizes, colors=colors, autopct=autopct_format, startangle=140
        )
        plt.axis("equal")  # Equal aspect ratio asegura que el gráfico sea un círculo

        # Agregar la leyenda con las cantidades totales
        plt.legend(
            wedges,
            labels,
            bbox_to_anchor=(0.2, 1.15),
        )

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
    if total != 0:
        porcentajes = [x["cant"]*100/total for x in lista]
    else:
        porcentajes = [0 for x in lista]

    fig, ax = plt.subplots()
    # ax.pie(porcentajes, labels=leyendas, autopct='%1.1f%%')

    plt.figure(figsize=(6, 6))
    wedges, texts, autotexts = plt.pie(
        porcentajes, autopct="%1.1f%%", startangle=140
    )
    plt.axis("equal")  # Equal aspect ratio asegura que el gráfico sea un círculo

    # Agregar la leyenda con las cantidades totales
    plt.legend(
        wedges,
        leyendas,
        bbox_to_anchor=(0.2, 1.15),
    )
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


@bp.get("/reporte_deudores")
def reporte_deudores():
    orden = request.args.get("orden", "asc")
    ordenar_por = request.args.get("ordenar_por", "id")
    pagina = convertir_a_entero(request.args.get("pagina", 1))
    cant_por_pag = int(request.args.get("por_pag", 6))

    jinetes, cant_resultados = listar_deudores(
        ordenar_por,
        orden,
        pagina,
        cant_por_pag,
    )

    cant_paginas = cant_resultados // cant_por_pag
    if cant_resultados % cant_por_pag != 0:
        cant_paginas += 1

    return render_template(
        "pages/estadisticas/reporte_deudores.html",
        jinetes=jinetes,
        cant_resultados=cant_resultados,
        cant_paginas=cant_paginas,
        pagina=pagina,
        orden=orden,
        ordenar_por=ordenar_por,
    )


@bp.get("/reporte_jinetes_dias")
def reporte_jinetes_por_dia():
    resultados_actuales = obtener_ranking_jinetes_por_dia()
    ranking_con_puestos = []

    for indice, item in enumerate(resultados_actuales, start=1):
        ranking_con_puestos.append(({"puesto" : indice,
                                     "dia": obtener_dia(item[0]).nombre,
                                     "cantidad": item[1]}))
    return render_template(
        "pages/estadisticas/ver_ranking_dias.html",
        ranking_actual=ranking_con_puestos,
        titulo="Reporte de propuestas de trabajo",
    )
