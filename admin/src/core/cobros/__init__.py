from src.core.database import db
from src.core.cobros.cobro import Cobro

''' 
    Funcion que lista todos los cobros del sistema. Recibe un parámetro booleano llamado orden_asc
    Si el parámetro es True, el orden es ascendente
    Si el parámetro es False, el orden es descendente
'''
def listar_cobros(orden_asc=1, pagina_inicial=1, por_pag=20):
    cobros_ordenados = Cobro.todos_paginados(orden_asc, pagina_inicial,por_pag)
    
    return cobros_ordenados


# función que crea un cobro
def crear_cobro(fecha_pago, medio_de_pago, monto, observaciones):
    cobro = Cobro(fecha_pago=fecha_pago, medio_de_pago=medio_de_pago, monto=monto, observaciones=observaciones)
    db.session.add(cobro)
    db.session.commit()
    
    return cobro

