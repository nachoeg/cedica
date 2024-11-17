from src.core.database import db
from src.core.jinetes_y_amazonas.jinetes_y_amazonas import (
    JineteOAmazona, Diagnostico, Dia, Familiar)
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


# función que crea un registro de jinete o amazona
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
        PuestoLaboral.nombre == "Profesor de Equitación"
    )
    print(profesores)
    return profesores


def listar_conductores():
    """
    Funcion que retorna los conductores del sistema.
    """
    conductores = Miembro.query.join(PuestoLaboral).filter(
        PuestoLaboral.nombre == "Conductor"
    )

    return conductores


def listar_auxiliares_pista():
    """
    Funcion que retorna los auxiliares de pista del sistema.
    """
    auxiliares = Miembro.query.join(PuestoLaboral).filter(
        PuestoLaboral.nombre == "Auxiliar de pista"
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
