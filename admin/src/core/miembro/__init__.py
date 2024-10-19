from src.core.database import db
from src.core.miembro.miembro import Miembro
from src.core.miembro.extras import CondicionDeTrabajo, Profesion, PuestoLaboral
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
    query = Miembro.query.join(Profesion)

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