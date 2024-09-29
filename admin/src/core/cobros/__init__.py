from src.core.database import db
from src.core.cobros.cobro import Cobro


def listar_cobros():
    cobros = Cobro.query.all()

    return cobros

def crear_cobro(**kwargs):
    cobro = Cobro(**kwargs)
    db.session.add(cobro)
    db.session.commit()

    return cobro

