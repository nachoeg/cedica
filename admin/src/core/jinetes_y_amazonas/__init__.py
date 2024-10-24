from src.core.database import db
from src.core.jinetes_y_amazonas.jinetes_y_amazonas import JineteOAmazona, Diagnostico
from src.core.jinetes_y_amazonas.documentos import Archivo_JYA, TipoArchivo
from src.core.miembro.miembro import Miembro
from src.core.miembro.extras import PuestoLaboral
from src.core.ecuestre.ecuestre import Ecuestre

# funcion que crea un diagnóstico médico
def crear_diagnostico(**kwargs):
    diagnostico = Diagnostico(**kwargs)
    db.session.add(diagnostico)
    db.session.commit()

    return diagnostico

# funcion que lista todos los jinetes o amazonas del sistema
def listar_j_y_a(nombre_filtro="", apellido_filtro="", dni_filtro="", profesional_filtro="", ordenar_por="id", orden="asc", pagina=1, cant_por_pag=10):
    query = JineteOAmazona.query.filter(
        JineteOAmazona.nombre.ilike(f"%{nombre_filtro}"),
        JineteOAmazona.apellido.ilike(f"%{apellido_filtro}"),
        JineteOAmazona.profesionales_a_cargo.ilike(f"%{profesional_filtro}"),
    )

    if dni_filtro != "":
        query = query.filter(JineteOAmazona.dni == dni_filtro)

    if orden == "asc":
        query = query.order_by(getattr(JineteOAmazona, ordenar_por).asc())
    else:
        query = query.order_by(getattr(JineteOAmazona, ordenar_por).desc())

    j_y_a_ordenados = query.paginate(page=pagina, per_page=cant_por_pag, error_out=False)
    
    return j_y_a_ordenados


# función que crea un registro de jinete o amazona
def crear_j_o_a(nombre, apellido, dni, edad, fecha_nacimiento, provincia_nacimiento, localidad_nacimiento, domicilio_actual, telefono_actual, contacto_emer_nombre, contacto_emer_telefono):
    j_o_a = JineteOAmazona(nombre=nombre, apellido=apellido, dni=dni, edad=edad, fecha_nacimiento=fecha_nacimiento, provincia_nacimiento=provincia_nacimiento, localidad_nacimiento=localidad_nacimiento, domicilio_actual=domicilio_actual, telefono_actual=telefono_actual, contacto_emer_nombre=contacto_emer_nombre, contacto_emer_telefono=contacto_emer_telefono)
    db.session.add(j_o_a)
    db.session.commit()

    return j_o_a

def cargar_informacion_salud(id, certificado_discapacidad, diagnostico_id, diagnostico_otro, tipo_discapacidad):
    jya = JineteOAmazona.query.get_or_404(id)
    jya.certificado_discapacidad = certificado_discapacidad
    jya.diagnostico_id = diagnostico_id
    jya.diagnostico_otro = diagnostico_otro
    jya.tipo_discapacidad = tipo_discapacidad

    db.session.commit()

def cargar_informacion_economica(id, asignacion_familiar, tipo_asignacion_familiar, beneficiario_pension,tipo_pension, obra_social, num_afiliado, posee_curatela, observaciones_obra_social):
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

def cargar_informacion_escuela(id, nombre_escuela, direccion_escuela, telefono_escuela, grado_escuela, observaciones_escuela, profesionales_a_cargo):
    jya = JineteOAmazona.query.get_or_404(id)
    jya.nombre_escuela = nombre_escuela
    jya.direccion_escuela = direccion_escuela
    jya.telefono_escuela = telefono_escuela
    jya.grado_escuela = grado_escuela
    jya.observaciones_escuela = observaciones_escuela
    jya.profesionales_a_cargo = profesionales_a_cargo
    db.session.commit()

def cargar_informacion_institucional(id, propuesta_de_trabajo, condicion, sede, dias, profesor_id, conductor_caballo_id, caballo_id, auxiliar_pista_id):
    jya = JineteOAmazona.query.get_or_404(id)
    jya.propuesta_de_trabajo = propuesta_de_trabajo
    jya.condicion = condicion
    jya.sede = sede
    #jya.dias = dias
    jya.profesor_id = profesor_id
    jya.conductor_caballo_id =conductor_caballo_id
    jya.caballo_id = caballo_id
    jya.auxiliar_pista_id = auxiliar_pista_id
    db.session.commit()

def eliminar_jya(id):
    jya = JineteOAmazona.query.get_or_404(id)
    db.session.delete(jya)
    db.session.commit()
    return jya

def encontrar_jya(id):
    jya = JineteOAmazona.query.get_or_404(id)
    return jya

def cargar_archivo(jya_id, titulo,tipo_archivo, url, archivo_externo):
    archivo = Archivo_JYA(titulo=titulo,jya_id=jya_id, tipo_archivo=tipo_archivo, url= url, externo=archivo_externo)
    db.session.add(archivo)
    db.session.commit()

def encontrar_archivos_de_jya(jya_id):
    jya = JineteOAmazona.query.get_or_404(jya_id)
    
    return jya.documentos

def encontrar_archivo(archivo_id):
    archivo = Archivo_JYA.query.get_or_404(archivo_id)
    
    return archivo

def listar_documentos(
    jya_id,
    nombre_filtro="",
    tipo_filtro="",
    ordenar_por="id",
    orden="asc",
    pagina=1,
    cant_por_pagina=10,
):
    query = Archivo_JYA.query.filter(
            Archivo_JYA.jya_id == jya_id,
            Archivo_JYA.titulo.ilike(f'%{nombre_filtro}%'),
        )
    if tipo_filtro != "":
        tipo = TipoArchivo(tipo_filtro).name
        query = query.filter(
            Archivo_JYA.tipo_archivo == tipo
        )
    
    cant_resultados = query.count()

    if orden == "asc":
        query = query.order_by(getattr(Archivo_JYA, ordenar_por).asc())
    else:
        query = query.order_by(getattr(Archivo_JYA, ordenar_por).desc())

    archivos = query.paginate(page=pagina, per_page=cant_por_pagina, error_out=False)
    return archivos, cant_resultados


def listar_tipos_de_documentos():
    tipos_de_documentos = TipoArchivo.listar()

    return tipos_de_documentos


def listar_diagnosticos():
    diagnosticos = Diagnostico.query.all()

    return diagnosticos

def listar_profesores():
    profesores = Miembro.query.join(PuestoLaboral).filter(
        PuestoLaboral.nombre == "Profesor de Equitación"
    )

    return profesores

def listar_conductores():
    conductores = Miembro.query.join(PuestoLaboral).filter(
        PuestoLaboral.nombre == "Conductor"
    )

    return conductores

def listar_auxiliares_pista():
    auxiliares = Miembro.query.join(PuestoLaboral).filter(
        PuestoLaboral.nombre == "Auxiliar de pista"
    )

    return auxiliares

def listar_caballos():
    caballos = Ecuestre.query.all()

    return caballos

def obtener_documento(doc_id):
    
    return Archivo_JYA.query.get_or_404(doc_id)

def eliminar_documento_j_y_a(doc_id):
    documento = Archivo_JYA.query.get(doc_id)
    db.session.delete(documento)
    db.session.commit()

    return documento