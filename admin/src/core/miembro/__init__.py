from src.core.database import db
from src.core.miembro.miembro import Miembro
from src.core.miembro.extras import CondicionDeTrabajo, Profesion, PuestoLaboral
from src.core.miembro.domicilio import Domicilio


def listar_miembros():
    miembros = Miembro.query.all()

    return miembros

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