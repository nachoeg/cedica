from src.core.database import db
from src.core.cobros.cobro import Cobro

# funcion que lista todos los cobros del sistema ordenados de manera ascendente
def listar_cobros():
    cobros = Cobro.query.all()
    cobros_ordenados = sorted(cobros, key= lambda x: x.fecha_pago)
    
    return cobros_ordenados


# función que crea un cobro
def crear_cobro(**kwargs):
    cobro = Cobro(**kwargs)
    db.session.add(cobro)
    db.session.commit()

    return cobro

