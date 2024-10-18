import string
from flask import render_template, request, redirect, url_for
from flask import Blueprint
from src.core.jinetes_y_amazonas import listar_j_y_a, crear_j_o_a, cargar_informacion_salud, cargar_informacion_economica, cargar_informacion_escuela, cargar_informacion_institucional, eliminar_jya, encontrar_jya
from src.core.jinetes_y_amazonas.jinetes_y_amazonas import JineteOAmazona, Diagnostico
from src.core.jinetes_y_amazonas.forms_jinetes import NuevoJYAForm, InfoSaludJYAForm, InfoEconomicaJYAForm, InfoEscolaridadJYAForm,InfoInstitucionalJYAForm
from src.core.miembro.miembro import Miembro
from src.core.ecuestre.ecuestre import Ecuestre

bp = Blueprint("jinetes_y_amazonas", __name__, url_prefix="/jinetes_y_amazonas")

'''
    Retorna los jinetes y amazonas
'''

@bp.get("/")
def listar():
    orden = request.args.get("orden", "asc")
    ordenar_por = request.args.get("ordenar_por", "id")
    pagina = int(request.args.get('pagina', 1))
    cant_por_pag = int(request.args.get('por_pag',10))
    nombre_filtro = request.args.get("nombre", "")

    jinetes = listar_j_y_a()
    cant_resultados = len(jinetes.items)
    cant_paginas = cant_resultados // cant_por_pag
    if cant_resultados % cant_por_pag != 0:
        cant_paginas += 1
    
        return render_template(
        "jinetes_y_amazonas/listar.html",
        jinetes=jinetes,
        cant_resultados=cant_resultados,
        cant_paginas=cant_paginas,
        pagina=pagina,
        orden=orden,
        ordenar_por=ordenar_por,
        nombre_filtro=nombre_filtro,
    )

@bp.route("/nuevo_joa", methods=["GET", "POST"])
def nuevo_j_y_a():
    form = NuevoJYAForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        apellido = form.apellido.data
        dni = form.dni.data
        edad = form.edad.data
        fecha_nacimiento = form.fecha_nacimiento.data
        provincia_nacimiento = form.provincia_nacimiento.data
        localidad_nacimiento = form.localidad_nacimiento.data
        domicilio_actual = form.domicilio_actual.data
        telefono_actual = form.telefono_actual.data
        contacto_emer_nombre = form.contacto_emer_nombre.data
        contacto_emer_telefono = form.contacto_emer_telefono.data
        jya_nuevo = crear_j_o_a(nombre, apellido, dni, edad, fecha_nacimiento, provincia_nacimiento, localidad_nacimiento, domicilio_actual, telefono_actual, contacto_emer_nombre, contacto_emer_telefono)

        return redirect(url_for('jinetes_y_amazonas.cargar_info_salud', id=jya_nuevo.id))

    return render_template("jinetes_y_amazonas/nuevo_j_y_a.html", form=form)

@bp.route("/cargar_info_salud/<string:id>", methods=["GET", "POST"])
def cargar_info_salud(id: string):
    form = InfoSaludJYAForm()
    form.diagnostico_id.choices = [(diagnostico.id, diagnostico.nombre) for diagnostico in Diagnostico.query.all()]
    if form.validate_on_submit():
        certificado_discapacidad = form.certificado_discapacidad.data
        diagnostico_id = form.diagnostico_id.data
        diagnostico_otro = form.diagnostico_otro.data
        tipo_discapacidad = form.tipo_discapacidad.data
        cargar_informacion_salud(id, certificado_discapacidad, diagnostico_id, diagnostico_otro, tipo_discapacidad)
        return redirect(url_for('jinetes_y_amazonas.cargar_info_econ', id=id))

    return render_template("jinetes_y_amazonas/nuevo_j_y_a_salud.html", form=form)

@bp.route("/cargar_info_econ/<string:id>", methods=["GET", "POST"])
def cargar_info_econ(id : string):
    form = InfoEconomicaJYAForm()

    if form.validate_on_submit():
        asignacion_familiar = form.asignacion_familiar.data
        tipo_asignacion_familiar = form.tipo_asignacion_familiar.data
        beneficiario_pension = form.beneficiario_pension.data
        tipo_pension = form.tipo_pension.data
        obra_social = form.obra_social.data
        num_afiliado = form.num_afiliado.data
        posee_curatela = form.posee_curatela.data
        observaciones_obra_social = form.observaciones_obra_social.data

        cargar_informacion_economica(id, asignacion_familiar, tipo_asignacion_familiar, beneficiario_pension,tipo_pension, obra_social, num_afiliado, posee_curatela, observaciones_obra_social)
        return redirect(url_for('jinetes_y_amazonas.cargar_info_esc', id= id))
    return render_template("jinetes_y_amazonas/nuevo_j_y_a_econ.html", form=form)

@bp.route("/cargar_info_esc/<string:id>", methods=["GET", "POST"])
def cargar_info_esc(id : string):
    form = InfoEscolaridadJYAForm()
    if form.validate_on_submit():
        nombre_escuela = form.nombre_escuela.data
        direccion_escuela = form.direccion_escuela.data
        telefono_escuela = form.telefono_escuela.data
        grado_escuela = form.grado_escuela.data
        observaciones_escuela = form.observaciones_escuela.data
        profesionales_a_cargo = form.profesionales_a_cargo.data
        cargar_informacion_escuela(id, nombre_escuela, direccion_escuela, telefono_escuela, grado_escuela, observaciones_escuela, profesionales_a_cargo)
        return redirect(url_for('jinetes_y_amazonas.cargar_info_inst', id = id))
    return render_template("jinetes_y_amazonas/nuevo_j_y_a_esc.html", form=form)


@bp.route("/cargar_info_inst/<string:id>", methods=["GET", "POST"])
def cargar_info_inst(id : string):
    form = InfoInstitucionalJYAForm()
    form.profesor_id.choices = [(profesor.id, profesor.nombre) for profesor in Miembro.query.all()]
    form.conductor_caballo_id.choices = [(conductor.id, conductor.nombre) for conductor in Miembro.query.all()]
    form.caballo_id.choices = [(caballo.id, caballo.nombre) for caballo in Ecuestre.query.all()]
    form.auxiliar_pista_id.choices = [(auxiliar.id, auxiliar.nombre) for auxiliar in Miembro.query.all()]
    if form.validate_on_submit():
        propuesta_de_trabajo = form.propuesta_trabajo.data
        condicion = form.condicion.data
        sede = form.sede.data
        profesor_id = form.profesor_id.data
        conductor_caballo_id = form.profesor_id.data
        caballo_id = form.caballo_id.data
        auxiliar_pista_id = form.auxiliar_pista_id.data
        dias = form.dias.data
        cargar_informacion_institucional(id, propuesta_de_trabajo, condicion, sede, dias, profesor_id, conductor_caballo_id, caballo_id, auxiliar_pista_id)
        return redirect(url_for('jinetes_y_amazonas.listar'))
    return render_template("jinetes_y_amazonas/nuevo_j_y_a_inst.html", form=form)
 

''' @bp.route("/editar_cobro/<string:id>", methods=["GET", "POST"])
def editar_cobro(id: str):
    cobro = encontrar_cobro(id)
    print(cobro)
    form = CobroForm(obj=cobro)
    form.joa.choices = [(joa.id, joa.nombre +" "+ joa.apellido) for joa in JineteOAmazona.query.order_by('nombre')]
    form.joa.data = cobro.joa.id
    form.medio_de_pago.data = cobro.medio_de_pago.name
    print("Antes de entrar")
    if request.method == "POST" and form.validate_on_submit():
        cobro.fecha_pago = form.fecha_pago.data
        cobro.medio_de_pago = form.medio_de_pago.data
        cobro.monto = form.monto.data
        cobro.observaciones = form.observaciones.data
        cobro.joa_id = form.joa.data
        guardar_cambios()

        return redirect(url_for('cobros.listar'))
    return render_template('cobros/crear_cobro.html', form=form)
 '''

@bp.get("/<int:id>/")
def ver(id: int):
    jya = encontrar_jya(id)
    return render_template("jinetes_y_amazonas/ver_jya.html", jya=jya)

@bp.route("/<int:id>/editar/", methods=["GET", "POST"])
def editar_jya(id:int):
    jya = encontrar_jya(id)
    return redirect(url_for('jinetes_y_amazonas.listar'))

@bp.get("/<int:id>/eliminar/")
def eliminar(id: int):
    eliminar_jya(id)
    return redirect(url_for("jinetes_y_amazonas.listar"))
