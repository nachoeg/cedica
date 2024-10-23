from src.core.database import db
from src.core.cobros.cobro import Cobro, MedioDePago
from src.core.jinetes_y_amazonas.jinetes_y_amazonas import JineteOAmazona
from src.core.miembro.miembro import Miembro

''' 
    Funcion que lista todos los cobros del sistema. Recibe un parámetro booleano llamado orden_asc
    Si el parámetro es True, el orden es ascendente
    Si el parámetro es False, el orden es descendente
'''
def listar_cobros(nombre_filtro="", apellido_filtro="", medio_pago_filtro="",despues_de_filtro="", antes_de_filtro="", ordenar_por="id", orden="asc", pagina=1, cant_por_pag=10
    ):

    query = Cobro.query.join(Miembro).filter(
        Miembro.nombre.ilike(f"%{nombre_filtro}%"),
        Miembro.apellido.ilike(f"%{apellido_filtro}%"),
    )
    if medio_pago_filtro != "":
        medio_pago = MedioDePago(medio_pago_filtro).name
        query = query.filter(
            Cobro.medio_de_pago == medio_pago
        )

    if despues_de_filtro != "":
        query = query.filter(
            Cobro.fecha_pago >= despues_de_filtro
        )
    
    if antes_de_filtro != "":
        query = query.filter(
            Cobro.fecha_pago <= antes_de_filtro
        )

    if orden == "asc":
        query = query.order_by(getattr(Cobro, ordenar_por).asc())
    else:
        query = query.order_by(getattr(Cobro, ordenar_por).desc())

    cobros_ordenados = query.paginate(page=pagina, per_page=cant_por_pag, error_out=False)

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

def cargar_joa_choices():
    
    return [(joa.id, joa.nombre +" "+ joa.apellido) for joa in JineteOAmazona.query.order_by('nombre')]

def cargar_miembro_choices():
    
    return [(miembro.id, miembro.nombre + " " + miembro.apellido) for miembro in Miembro.query.order_by('nombre')]

def listar_medios_de_pago():
    
    return MedioDePago.listar()
