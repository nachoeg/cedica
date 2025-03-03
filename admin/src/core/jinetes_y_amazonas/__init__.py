from sqlalchemy import func
from src.core.database import db
from src.core.jinetes_y_amazonas.jinetes_y_amazonas import (
    JineteOAmazona, Diagnostico, Dia, Familiar, TipoDeDiscapacidad)
from src.core.jinetes_y_amazonas.documentos import Archivo_JYA, TipoArchivo
from src.core.miembro.miembro import Miembro
from src.core.miembro.extras import PuestoLaboral
from src.core.ecuestre.ecuestre import Ecuestre


def crear_diagnostico(**kwargs):
    """
    Funcion que crea un diagnóstico médico.
    """
    diagnostico = Diagnostico(**kwargs)
    db.session.add(diagnostico)
    db.session.commit()

    return diagnostico


def crear_dia(**kwargs):
    """
    Función que crea un día de la semana
    """
    dia = Dia(**kwargs)
    db.session.add(dia)
    db.session.commit()

    return dia


def crear_tipo_discapacidad(**kwargs):
    """
    Funcion que crea un tipo de discapacidad.
    """
    tipo_de_discapacidad = TipoDeDiscapacidad(**kwargs)
    db.session.add(tipo_de_discapacidad)
    db.session.commit()

    return tipo_de_discapacidad


def listar_j_y_a(
    nombre_filtro="",
    apellido_filtro="",
    dni_filtro="",
    profesional_filtro="",
    ordenar_por="id",
    orden="asc",
    pagina=1,
    cant_por_pag=6,
):
    """
    Funcion que devuelve el listado de
    jinetes y amazonas filtrado a partir
    de los parámetros recibidos y ordenado según los parámetros recibidos.
    """
    query = JineteOAmazona.query.filter(
        JineteOAmazona.nombre.ilike(f"%{nombre_filtro}%"),
        JineteOAmazona.apellido.ilike(f"%{apellido_filtro}%"),
    )

    if profesional_filtro != "":
        query = query.filter(
            JineteOAmazona.profesionales_a_cargo.ilike(
                f"%{profesional_filtro}%")
        )

    if dni_filtro != "":
        query = query.filter(JineteOAmazona.dni == dni_filtro)

    if orden == "asc":
        query = query.order_by(getattr(JineteOAmazona, ordenar_por).asc())
    else:
        query = query.order_by(getattr(JineteOAmazona, ordenar_por).desc())

    cant_resultados = query.count()

    j_y_a_ordenados = query.paginate(
        page=pagina, per_page=cant_por_pag, error_out=False
    )

    return j_y_a_ordenados, cant_resultados


def crear_j_o_a(
    nombre,
    apellido,
    dni,
    fecha_nacimiento,
    provincia_nacimiento,
    localidad_nacimiento,
    domicilio_actual,
    telefono_actual,
    contacto_emer_nombre,
    contacto_emer_telefono,
    becado,
    porcentaje_beca=0
):
    """
    Funcion que crea un registro en la tabla de jinetes y amazonas
    a partir de los parámetros recibidos,
    a partir de cargar la información general del jinete y amazona:
    nombre, apellido, dni, edad, fecha de nacimiento,
    provincia y localidad de nacimiento,
    domicilio y telefono actuales y contacto de emergencia.
    """
    j_o_a = JineteOAmazona(
        nombre=nombre,
        apellido=apellido,
        dni=dni,
        fecha_nacimiento=fecha_nacimiento,
        provincia_nacimiento=provincia_nacimiento,
        localidad_nacimiento=localidad_nacimiento,
        domicilio_actual=domicilio_actual,
        telefono_actual=telefono_actual,
        contacto_emer_nombre=contacto_emer_nombre,
        contacto_emer_telefono=contacto_emer_telefono,
        becado=becado,
        porcentaje_beca=porcentaje_beca
    )
    db.session.add(j_o_a)
    db.session.commit()

    return j_o_a


def cargar_tipo_discapacidad(jya, tipo_discapacidad):
    """
    Agrega un tipo de discapacidad a los tipos de discapacidad
    de un jinete pasado por parámetro.
    Tipo de discapacidad es un número del 1 al 4 correspondientes
    a los tipos de discapacidad Mental, Motora, Sensorial y Visceral
    """
    jya.tipo_discapacidad.append(obtener_tipo_discapacidad(tipo_discapacidad))
    db.session.commit()

    return jya


def cargar_dia_a_jinete(jya, dia):
    """
    Agrega un día a los días asignados al jinete recibido
    como parámetro. 
    El día es un número entre 1 y 7 correspondiente a Lunes, 
    Martes, Miercoles, Jueves, Viernes, Sabado y Domingo
    """
    jya.dias_asignados.append(obtener_dia(dia))
    db.session.commit()

    return jya


def cargar_deuda(jya, tiene_deuda):
    """
    Recibe un jinete por parámetro y le asigna el valor del segundo
    parámetro al campo tiene_deuda del jinete.
    """
    jya.tiene_deuda = tiene_deuda
    db.session.commit()

    return jya


def cargar_propuesta_trabajo(jya, propuesta):
    """
    Recibe un jinete por parámetro y le asigna el valor
    del segundo parámetro al campo propuesta_trabajo.
    El parámetro propuesta puede tomar los valores 'hipoterapia',
    'monta_terapeutica', 'deporte_ecuestre',
    'actividades_recreativas', 'equitacion'
    """
    jya.propuesta_trabajo = propuesta
    db.session.commit()


def cargar_condicion(jya, condicion):
    """
    Recibe un jinete por parámetro y le asigna el valor
    del segundo parámetro al campo condicion: puede ser 'regular' o 'de_baja'
    """
    jya.condicion = condicion
    db.session.commit()


def cargar_informacion_salud(
    id, certificado_discapacidad,
    diagnostico_id, diagnostico_otro, tipo_discapacidad
):
    """
    Funcion que, dado un jinete y amazona,
    carga la información de salud en el registro correspondiente.
    """
    jya = JineteOAmazona.query.get_or_404(id)
    jya.certificado_discapacidad = certificado_discapacidad
    jya.diagnostico_id = diagnostico_id
    jya.diagnostico_otro = diagnostico_otro
    jya.tipo_discapacidad = tipo_discapacidad

    db.session.commit()


def cargar_informacion_economica(
    id,
    asignacion_familiar,
    tipo_asignacion_familiar,
    beneficiario_pension,
    tipo_pension,
    obra_social,
    num_afiliado,
    posee_curatela,
    observaciones_obra_social,
):
    """
    Funcion que, dado un jinete y amazona, carga
    la información económica en el registro correspondiente.
    """
    jya = JineteOAmazona.query.get_or_404(id)
    jya.asignacion_familiar = asignacion_familiar
    jya.tipo_asignacion_familiar = tipo_asignacion_familiar
    jya.beneficiario_pension = beneficiario_pension
    jya.tipo_pension = tipo_pension
    jya.obra_social = obra_social
    jya.num_afiliado = num_afiliado
    jya.posee_curatela = posee_curatela
    jya.observaciones_obra_social = observaciones_obra_social
    db.session.commit()


def cargar_informacion_escuela(
    id,
    nombre_escuela,
    direccion_escuela,
    telefono_escuela,
    grado_escuela,
    observaciones_escuela,
    profesionales_a_cargo,
):
    """
    Funcion que, dado un jinete y amazona,
    carga la información relacionada a la escolaridad
    del jinete o de la amazona, en el registro correspondiente.
    """
    jya = JineteOAmazona.query.get_or_404(id)
    jya.nombre_escuela = nombre_escuela
    jya.direccion_escuela = direccion_escuela
    jya.telefono_escuela = telefono_escuela
    jya.grado_escuela = grado_escuela
    jya.observaciones_escuela = observaciones_escuela
    jya.profesionales_a_cargo = profesionales_a_cargo
    db.session.commit()


def cargar_informacion_institucional(
    id,
    propuesta_de_trabajo,
    condicion,
    sede,
    dias,
    profesor_id,
    conductor_caballo_id,
    caballo_id,
    auxiliar_pista_id,
):
    """
    Funcion que, dado un jinete y amazona,
    carga la información institucional relacionada
    al jinete o amazona, en el registro correspondiente.
    """
    jya = JineteOAmazona.query.get_or_404(id)
    jya.propuesta_de_trabajo = propuesta_de_trabajo
    jya.condicion = condicion
    jya.sede = sede
    jya.dias_asignados = dias
    jya.profesor_id = profesor_id
    jya.conductor_caballo_id = conductor_caballo_id
    jya.caballo_id = caballo_id
    jya.auxiliar_pista_id = auxiliar_pista_id
    db.session.commit()


def guardar_cambios():
    """
    Funcion que guarda los cambios en la base de datos.
    """
    db.session.commit()


def eliminar_jya(id):
    """
    Funcion que, dado un id, elimina el jinete o la amazona con dicho id.
    """
    jya = JineteOAmazona.query.get_or_404(id)
    db.session.delete(jya)
    db.session.commit()
    return jya


def encontrar_jya(id):
    """
    Funcion que busca y retorna un jinete o amazona por su id.
    """
    jya = JineteOAmazona.query.get_or_404(id)
    return jya


def cargar_archivo(jya_id, titulo, tipo_archivo, url, archivo_externo):
    """
    Funcion que, dado un jinete y amazona,
    carga la información de salud en el registro correspondiente.
    """
    archivo = Archivo_JYA(
        titulo=titulo,
        jya_id=jya_id,
        tipo_archivo=tipo_archivo,
        url=url,
        externo=archivo_externo,
    )
    db.session.add(archivo)
    db.session.commit()


def encontrar_archivos_de_jya(jya_id):
    """
    Funcion que, dado el id de un jinete o amazona,
    retorna los documentos asociados a él.
    """
    jya = JineteOAmazona.query.get_or_404(jya_id)

    return jya.documentos


def encontrar_archivo(archivo_id):
    """
    Funcion que busca y retorna un documento dado su id.
    """
    archivo = Archivo_JYA.query.get_or_404(archivo_id)

    return archivo


def listar_documentos(
    jya_id,
    nombre_filtro="",
    tipo_filtro="",
    ordenar_por="id",
    orden="asc",
    pagina=1,
    cant_por_pagina=6,
):
    """
    Funcion que, dado un jinete y determinados filtros,
    retorna un listado de documentos.
    """
    query = Archivo_JYA.query.filter(
        Archivo_JYA.jya_id == jya_id,
        Archivo_JYA.titulo.ilike(f"%{nombre_filtro}%"),
    )
    if tipo_filtro != "":
        tipo = TipoArchivo(tipo_filtro).name
        query = query.filter(Archivo_JYA.tipo_archivo == tipo)

    cant_resultados = query.count()

    if orden == "asc":
        query = query.order_by(getattr(Archivo_JYA, ordenar_por).asc())
    else:
        query = query.order_by(getattr(Archivo_JYA, ordenar_por).desc())

    archivos = query.paginate(page=pagina,
                              per_page=cant_por_pagina, error_out=False)
    return archivos, cant_resultados


def listar_tipos_de_documentos():
    """
    Funcion que retorna una lista con los tipos de documentos
    del módulo de jinetes y amazonas.
    """
    tipos_de_documentos = TipoArchivo.listar()

    return tipos_de_documentos


def listar_diagnosticos():
    """
    Funcion que devuelve el listado de diagnósticos del sistema.
    """
    diagnosticos = Diagnostico.query.all()

    return diagnosticos


def cargar_id_diagnostico_otro():
    """
        Función que retorna el id del diagnóstico con nombre "Otro"
    """
    diagnostico_otro = Diagnostico.query.where(
        Diagnostico.nombre == "Otro").first()

    return diagnostico_otro.id


def listar_profesores():
    """
    Funcion que retorna los profesores del sistema.
    """
    profesores = Miembro.query.join(PuestoLaboral).filter(
        PuestoLaboral.nombre == "Profesor de Equitación",
        Miembro.activo.is_(True)
    )

    return profesores


def listar_conductores():
    """
    Funcion que retorna los conductores del sistema.
    """
    conductores = Miembro.query.join(PuestoLaboral).filter(
        PuestoLaboral.nombre == "Conductor",
        Miembro.activo.is_(True)
    )

    return conductores


def listar_auxiliares_pista():
    """
    Funcion que retorna los auxiliares de pista del sistema.
    """
    auxiliares = Miembro.query.join(PuestoLaboral).filter(
        PuestoLaboral.nombre == "Auxiliar de pista",
        Miembro.activo.is_(True)
    )

    return auxiliares


def listar_caballos():
    """
    Funcion que retorna la lista de caballos del sistema.
    """
    caballos = Ecuestre.query.all()

    return caballos


def listar_dias():
    """
    Función que retorna el listado de días.
    """
    dias = Dia.query.all()

    return dias


def obtener_dia(dia_id):
    """
    Función que retorna un día a partir del id
    """
    dia = Dia.query.get_or_404(dia_id)

    return dia


def listar_tipos_de_discapacidad():
    """
    Función que retorna el listado de los tipos de discapacidad.
    """
    tipos = TipoDeDiscapacidad.query.all()

    return tipos


def eliminar_documento_j_y_a(doc_id):
    """
    Funcion que elimina un documento a partir de conocer su id.
    """
    documento = Archivo_JYA.query.get(doc_id)
    db.session.delete(documento)
    db.session.commit()

    return documento


def crear_familiar(
                jya_id,
                nombre,
                apellido,
                parentesco,
                dni,
                domicilio,
                telefono,
                email,
                nivel_escolaridad,
                ocupacion):
    """
    Función que crea un familiar de un jinete y amazona
    y la guarda en la base de datos
    """

    familiar = Familiar(
        jya_id=jya_id,
        nombre=nombre,
        apellido=apellido,
        parentesco=parentesco,
        dni=dni,
        domicilio_actual=domicilio,
        telefono_actual=telefono,
        email=email,
        nivel_escolaridad=nivel_escolaridad,
        ocupacion=ocupacion
    )
    db.session.add(familiar)
    db.session.commit()

    return familiar


def encontrar_familiar(id):
    """
    Funcion que retorna el familiar de un jinete/amazona
    dado el id del familiar
    """
    familiar = Familiar.query.get_or_404(id)

    return familiar


def listar_familiares(jya_id,
                      ordenar_por="id",
                      orden="asc",
                      pagina=1,
                      cant_por_pagina=6):
    """
    Funcion que retorna todos los familiares de un jinete/amazona
    dado el id del jinete/amazona
    """
    query = Familiar.query.filter(
        Familiar.jya_id == jya_id
    )

    cant_resultados = query.count()

    if orden == "asc":
        query = query.order_by(getattr(Familiar, ordenar_por).asc())
    else:
        query = query.order_by(getattr(Familiar, ordenar_por).desc())

    familiares = query.paginate(page=pagina,
                                per_page=cant_por_pagina, error_out=False)

    return familiares, cant_resultados


def obtener_tipo_discapacidad(tipo_id):
    """
    Funcion que retorna un tipo de discapacidad a partir del id
    """
    tipo = TipoDeDiscapacidad.query.get_or_404(tipo_id)

    return tipo


def obtener_ranking_propuestas():
    """
    Función que retorna el listado de propuestas de trabajo con su
    correspondiente cantidad de jinetes y amazonas que participan de ella
    ordenadas de manera descendente por el número de jinetes y amazonas.
    """
    propuestas = ["hipoterapia",
                  "monta_terapeutica",
                  "deporte_ecuestre",
                  "actividades_recreativas",
                  "equitacion"]

    propuestas_a_imprimir = {
                  "hipoterapia": "Hipoterapia",
                  "monta_terapeutica": "Monta terapéutica",
                  "deporte_ecuestre": "Deporte ecuestre",
                  "actividades_recreativas": "Actividades recreativas",
                  "equitacion": "Equitación"
    }
    ranking_historico = []
    ranking_actual = []
    for propuesta in propuestas:
        clave = propuestas_a_imprimir[propuesta]
        valor_historico = JineteOAmazona.query.filter(
            JineteOAmazona.propuesta_trabajo == propuesta).count()
        valor_actual = JineteOAmazona.query.filter(
            JineteOAmazona.propuesta_trabajo == propuesta,
            JineteOAmazona.condicion == "regular").count()
        ranking_historico.append((clave, valor_historico))
        ranking_actual.append((clave, valor_actual))

    ranking_historico.sort(key=lambda propuesta: propuesta[1], reverse=True)
    ranking_actual.sort(key=lambda propuesta: propuesta[1], reverse=True)

    return ranking_actual, ranking_historico


def obtener_cant_tipos_discapacidad():
    """
    Función que retorna el listado de tipos de discapacidad (el id de la tabla)
    con su correspondiente cantidad de jinetes y amazonas
    """
    tipos_dis_cantidades = TipoDeDiscapacidad.query.join(
        JineteOAmazona.tipo_discapacidad).with_entities(
        TipoDeDiscapacidad.id,
        func.count(JineteOAmazona.id)).group_by(TipoDeDiscapacidad.id).all()

    return tipos_dis_cantidades


def obtener_jinetes_por_tipo_discapacidad(tipo):
    """
    Función que imprime un listado de jinetes para cada tipo de discapacidad
    """
    for tipo in listar_tipos_de_discapacidad():
        JineteOAmazona.query.join(
            JineteOAmazona.tipo_discapacidad).filter(
            TipoDeDiscapacidad.id == tipo.id
        ).all()


def obtener_tipos_discapacidad():
    """
    Función que retorna los id y los nombres de todos los tipos de discapacidad
    """

    query = TipoDeDiscapacidad.query.with_entities(
        TipoDeDiscapacidad.id, TipoDeDiscapacidad.nombre).all()
    return query


def obtener_cantidad_becados():
    """
    Función que obtiene la cantidad de Jinetes y Amazonas becados y no becados.
    """
    total_becados = db.session.query(
        JineteOAmazona).filter_by(becado=True).count()
    total_no_becados = db.session.query(
        JineteOAmazona).filter_by(becado=False).count()

    return total_becados, total_no_becados


def listar_deudores(
    ordenar_por="id",
    orden="asc",
    pagina=1,
    cant_por_pag=6,
):
    """
    Funcion que devuelve el listado de
    jinetes y amazonas con deudas partir
    ordenado según los parámetros recibidos.
    """
    query = JineteOAmazona.query.filter(JineteOAmazona.tiene_deuda)

    if orden == "asc":
        query = query.order_by(getattr(JineteOAmazona, ordenar_por).asc())
    else:
        query = query.order_by(getattr(JineteOAmazona, ordenar_por).desc())

    cant_resultados = query.count()

    j_y_a_ordenados = query.paginate(
        page=pagina, per_page=cant_por_pag, error_out=False
    )

    return j_y_a_ordenados, cant_resultados


def obtener_ranking_jinetes_por_dia():
    """
    Función que retorna un ranking de días según la cantidad de jinetes
    que asisten a CEDICA.
    """
    jinetes_actuales = Dia.query.join(
        JineteOAmazona.dias_asignados).with_entities(
        Dia.id, func.count(JineteOAmazona.id)).group_by(
            Dia.id).filter(JineteOAmazona.condicion == 'regular').all()

    jinetes_historicos = Dia.query.join(
        JineteOAmazona.dias_asignados).with_entities(
        Dia.id, func.count(JineteOAmazona.id)).group_by(Dia.id).all()

    return jinetes_actuales, jinetes_historicos
