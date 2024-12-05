from datetime import datetime
from src.core.database import db
from src.core.miembro.miembro import Miembro
from src.core.miembro.extras import (
    CondicionDeTrabajo,
    Profesion,
    PuestoLaboral,
    TipoDeDocumentoMiembro,
    DocumentoMiembro,
)
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
    cant_por_pagina=10,
):
    """Lista los miembros de forma pagina, listando por defecto 10 miembros por pagina,
    se aplican distintos filtros, como por nombre, apellido, dni, email o profesion"""
    query = Miembro.query.join(Profesion)

    if nombre_filtro:
        query = query.filter(Miembro.nombre.ilike(f"%{nombre_filtro}%"))

    if apellido_filtro:
        query = query.filter(Miembro.apellido.ilike(f"%{apellido_filtro}%"))

    if dni_filtro:
        query = query.filter(Miembro.dni == int(dni_filtro))

    if email_filtro:
        query = query.filter(Miembro.email.ilike(f"%{email_filtro}%"))

    if profesion_filtro:
        query = query.filter(Profesion.nombre.ilike(f"%{profesion_filtro}%"))

    cant_resultados = query.count()

    # Manejo de paginación
    cant_paginas = (
        1
        if cant_resultados == 0
        else (
            cant_resultados // cant_por_pagina + (cant_resultados % cant_por_pagina > 0)
        )
    )

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
    cant_por_pagina=6,
):
    """Listao todos los documentos asignados a un usuarios, utiliza filtros para buscar un documento por nombre o tipo"""
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
    """Crea un nuevo miembro y lo guarda en la base de datos"""
    miembro = Miembro(**kwargs)
    db.session.add(miembro)
    db.session.commit()

    return miembro


def listar_profesiones():
    """Lista todas las profesiones posibles de un miembro"""
    profesiones = Profesion.query.all()
    return profesiones


def listar_puestos_laborales():
    """Lista todos los puestos laborales posibles de un miembro"""
    puestos = PuestoLaboral.query.all()
    return puestos


def listar_condiciones():
    """Lista todas las condiciones de trabajo posibles de un miembro"""
    condiciones = CondicionDeTrabajo.query.all()
    return condiciones


def crear_profesion(nombre):
    """Crea una nueva profesion"""
    profesion = Profesion(nombre=nombre)
    db.session.add(profesion)
    db.session.commit()
    return profesion


def crear_puesto_laboral(nombre):
    """Crea un nuevo puesto laboral"""
    puesto = PuestoLaboral(nombre=nombre)
    db.session.add(puesto)
    db.session.commit()
    return puesto


def crear_condicion(nombre):
    """Crea una nueva condicion de trabajo"""
    condicion = CondicionDeTrabajo(nombre=nombre)
    db.session.add(condicion)
    db.session.commit()
    return condicion


def crear_domicilio(**kwargs):
    """Crea un nuevo domicilio"""
    domicilio = Domicilio(**kwargs)
    db.session.add(domicilio)
    db.session.commit()

    return domicilio


def guardar_cambios():
    """Guarda los cambios en la base de datos"""
    db.session.commit()


def obtener_miembro(id):
    """Obtiene un miembro a parit del ID"""
    miembro = Miembro.query.filter_by(id=id).filter(Miembro.activo.is_(True)).first()
    return miembro


def obtener_miembro_dni(dni):
    """Obtiene un miembro a partir del dni"""
    miembro = Miembro.query.filter_by(dni=dni, activo=True).first()
    return miembro


def miembro_por_id(id):
    """Busca un miembro por id"""
    return Miembro.query.get_or_404(id)


def buscar_domicilio(calle, numero, piso, dpto, localidad):
    """A partir de ciertos datos dados, busca si equiste un domicilio cargado en el sistema con los mismos datos"""
    return Domicilio.query.filter_by(
        calle=calle, numero=numero, piso=piso, dpto=dpto, localidad=localidad
    ).first()


def cambiar_condicion_miembro(id):
    """Cambia la condicion de un miembro, de activo a inactivo y viceversa"""
    miembro = Miembro.query.get_or_404(id)
    if miembro.activo == True:
        miembro.activo = False
    else:
        miembro.activo = True
    db.session.commit()


def listar_tipos_de_documentos():
    """Lista todos los tipos de documentos"""
    tipos_de_documentos = TipoDeDocumentoMiembro.query.all()
    return tipos_de_documentos


def crear_tipo_de_documento(tipo):
    """Crea un nuevo tipo de documento"""
    tipo_de_documento = TipoDeDocumentoMiembro(tipo=tipo)
    db.session.add(tipo_de_documento)
    db.session.commit()
    return tipo_de_documento


def crear_documento(nombre, tipo_de_documento_id, url, miembro_id, archivo_externo):
    """Guarda un documento en el sistema"""
    documento = DocumentoMiembro(
        nombre=nombre,
        fecha=datetime.now(),
        tipo_de_documento_id=tipo_de_documento_id,
        url=url,
        miembro_id=miembro_id,
        archivo_externo=archivo_externo,
    )
    db.session.add(documento)
    db.session.commit()
    return documento


def obtener_documento(id):
    """Busca un documento por id"""
    documento = DocumentoMiembro.query.get_or_404(id)
    return documento


def eliminar_documento_miembro(documento_id):
    """Elimina un documento del sistema, buscandolo por id"""
    documento = DocumentoMiembro.query.get_or_404(documento_id)
    db.session.delete(documento)
    db.session.commit()
    return documento


def listar_miembros_habilitados():
    """Lista todos los miembors del sistema que estan habilitados"""
    miembros = Miembro.query.filter(Miembro.activo.is_(True)).all()
    return miembros
