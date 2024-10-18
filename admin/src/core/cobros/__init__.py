from src.core.database import db
from src.core.cobros.cobro import Cobro
from src.core.jinetes_y_amazonas.jinetes_y_amazonas import JineteOAmazona

''' 
    Funcion que lista todos los cobros del sistema. Recibe un parámetro booleano llamado orden_asc
    Si el parámetro es True, el orden es ascendente
    Si el parámetro es False, el orden es descendente
'''
def listar_cobros(orden_asc=1, pagina_inicial=1, por_pag=20):
    cobros_ordenados = Cobro.todos_paginados(orden_asc, pagina_inicial,por_pag)
    
    return cobros_ordenados


# función que crea un cobro
def crear_cobro(fecha_pago, medio_de_pago, monto, observaciones, joa_id, recibio_el_dinero_id):
    cobro = Cobro(fecha_pago=fecha_pago, medio_de_pago=medio_de_pago, monto=monto, observaciones=observaciones, joa_id=joa_id, recibio_el_dinero_id=recibio_el_dinero_id)
    db.session.add(cobro)
    db.session.commit()
    
    return cobro

def encontrar_cobro(id):
    return db.get_or_404(Cobro, id)

def guardar_cambios():
    db.session.commit()

def marcar_deuda(joa_id):
    jya = db.get_or_404(JineteOAmazona, joa_id)
    jya.tiene_deuda = True
    db.session.commit()


