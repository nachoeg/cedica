from datetime import datetime
from src.core.database import db
from src.core.miembro.miembro import Miembro
from src.core.miembro.extras import CondicionDeTrabajo, Profesion, PuestoLaboral, TipoDeDocumentoMiembro, DocumentoMiembro
from src.core.miembro.domicilio import Domicilio

def listar_miembros(
    nombre_filtro="",
    apellido_filtro="",
    dni_filtro="",
    email_filtro="",
    profesion_filtro="",
    ordenar_por="nombre",
    orden="asc",
    pagina=1,
    cant_por_pagina=10
):
    query = Miembro.query.join(Profesion).filter(Miembro.activo.is_(True))

    if nombre_filtro:
        query = query.filter(Miembro.nombre.ilike(f'%{nombre_filtro}%'))

    if apellido_filtro:
        query = query.filter(Miembro.apellido.ilike(f'%{apellido_filtro}%'))

    if dni_filtro:
        query = query.filter(Miembro.dni == int(dni_filtro))

    if email_filtro:
        query = query.filter(Miembro.email.ilike(f'%{email_filtro}%'))

    if profesion_filtro:
        query = query.filter(Profesion.nombre.ilike(f'%{profesion_filtro}%'))

    cant_resultados = query.count()

    # Manejo de paginación
    cant_paginas = 1 if cant_resultados == 0 else (cant_resultados // cant_por_pagina + (cant_resultados % cant_por_pagina > 0))

    if orden == "asc":
        query = query.order_by(getattr(Miembro, ordenar_por).asc())
    else:
        query = query.order_by(getattr(Miembro, ordenar_por).desc())

    miembros = query.paginate(page=pagina, per_page=cant_por_pagina, error_out=False)
    return miembros, cant_resultados

def listar_documentos(
    miembro_id,
    nombre_filtro="",
    tipo_filtro="",
    ordenar_por="id",
    orden="asc",
    pagina=1,
    cant_por_pagina=10,
):
    query = DocumentoMiembro.query.join(TipoDeDocumentoMiembro).filter(
        DocumentoMiembro.miembro_id == miembro_id,
        DocumentoMiembro.nombre.ilike(f"%{nombre_filtro}%"),
        TipoDeDocumentoMiembro.tipo.ilike(f"%{tipo_filtro}%"),
    )

    cant_resultados = query.count()

    if orden == "asc":
        query = query.order_by(getattr(DocumentoMiembro, ordenar_por).asc())
    else:
        query = query.order_by(getattr(DocumentoMiembro, ordenar_por).desc())

    documentos = query.paginate(page=pagina, per_page=cant_por_pagina, error_out=False)
    return documentos, cant_resultados

def crear_miembro(**kwargs):
    miembro = Miembro(**kwargs)
    db.session.add(miembro)
    db.session.commit()

    return miembro

def listar_profesiones():
    profesiones = Profesion.query.all()
    return profesiones

def listar_puestos_laborales():
    puestos = PuestoLaboral.query.all()
    return puestos

def listar_condiciones():
    condiciones = CondicionDeTrabajo.query.all()
    return condiciones

def crear_profesion(nombre):
    profesion = Profesion(nombre=nombre)
    db.session.add(profesion)
    db.session.commit()
    return profesion

def crear_puesto_laboral(nombre):
    puesto = PuestoLaboral(nombre=nombre)
    db.session.add(puesto)
    db.session.commit()
    return puesto

def crear_condicion(nombre):
    condicion = CondicionDeTrabajo(nombre=nombre)
    db.session.add(condicion)
    db.session.commit()
    return condicion

def crear_domicilio(**kwargs):
    domicilio = Domicilio(**kwargs)
    db.session.add(domicilio)
    db.session.commit()

    return domicilio

def guardar_cambios():
    db.session.commit()

def obtener_miembro(id):
    miembro = Miembro.query.get(id)
    return miembro

def obtener_miembro_dni(dni):
    miembro = Miembro.query.filter_by(dni=dni).first()
    return miembro

def buscar_domicilio(calle, numero, piso, dpto, localidad):
    return Domicilio.query.filter_by(
            calle=calle,
            numero=numero,
            piso=piso,
            dpto=dpto,
            localidad=localidad
        ).first()

def eliminar_miembro(id):
    miembro = Miembro.query.get(id)
    miembro.activo = False;
    db.session.commit()

def listar_tipos_de_documentos():
    tipos_de_documentos = TipoDeDocumentoMiembro.query.all()
    return tipos_de_documentos

def crear_tipo_de_documento(tipo):
    tipo_de_documento = TipoDeDocumentoMiembro(tipo=tipo)
    db.session.add(tipo_de_documento)
    db.session.commit()
    return tipo_de_documento

def crear_documento(nombre, tipo_de_documento_id, url, miembro_id):
    documento = DocumentoMiembro(
        nombre=nombre,
        fecha=datetime.now(),
        tipo_de_documento_id=tipo_de_documento_id,
        url=url,
        miembro_id=miembro_id,
    )
    db.session.add(documento)
    db.session.commit()
    return documento

def obtener_documento(id):
    documento = DocumentoMiembro.query.get(id)
    return documento