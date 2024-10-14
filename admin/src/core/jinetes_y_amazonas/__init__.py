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

    return j_o_a.id

def cargar_informacion_salud(id, certificado_discapacidad, diagnostico_id, diagnostico_otro, tipo_discapacidad):
    jya = JineteOAmazona.query.get_or_404(id)
    jya.certificado_discapacidad = certificado_discapacidad
    jya.diagnostico_id = diagnostico_id
    jya.diagnostico_otro = diagnostico_otro
    jya.tipo_discapacidad = tipo_discapacidad

    db.session.commit()

def cargar_informacion_economica(**kwargs):
    return ""

def cargar_informacion_escuela(**kwargs):
    return ""

def cargar_informacion_institucional(**kwargs):
    return ""