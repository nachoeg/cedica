from src.core.database import db
from src.core.jinetes_y_amazonas.jinetes_y_amazonas import JineteOAmazona, Diagnostico

# funcion que crea un diagnóstico médico
def crear_diagnostico(**kwargs):
    diagnostico = Diagnostico(**kwargs)
    db.session.add(diagnostico)
    db.session.commit()

    return diagnostico

# funcion que lista todos los jinetes o amazonas del sistema
def listar_j_y_a(orden_asc=1, pagina_inicial=1, por_pag=20):
    j_y_a = JineteOAmazona.todos_paginados(orden_asc, pagina_inicial,por_pag)
    
    return j_y_a


# función que crea un registro de jinete o amazona
def crear_j_o_a(nombre, apellido, dni, edad, fecha_nacimiento, provincia_nacimiento, localidad_nacimiento, domicilio_actual, telefono_actual, contacto_emer_nombre, contacto_emer_telefono):
    j_o_a = JineteOAmazona(nombre=nombre, apellido=apellido, dni=dni, edad=edad, fecha_nacimiento=fecha_nacimiento, provincia_nacimiento=provincia_nacimiento, localidad_nacimiento=localidad_nacimiento, domicilio_actual=domicilio_actual, telefono_actual=telefono_actual, contacto_emer_nombre=contacto_emer_nombre, contacto_emer_telefono=contacto_emer_telefono)
    db.session.add(j_o_a)
    db.session.commit()
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