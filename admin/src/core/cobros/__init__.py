from src.core.database import db
from src.core.cobros.cobro import Cobro, MedioDePago
from src.core.jinetes_y_amazonas.jinetes_y_amazonas import JineteOAmazona
from src.core.miembro.miembro import Miembro


def listar_cobros(
    nombre_filtro="",
    apellido_filtro="",
    medio_pago_filtro="",
    despues_de_filtro="",
    antes_de_filtro="",
    ordenar_por="id",
    orden="asc",
    pagina=1,
    cant_por_pag=10,
):
    """
    Funcion que lista todos los cobros del sistema. Recibe como parámetros filtros que ingresa el usuario
    y devuelve los cobros ordenados por id o por fecha de pago, en orden ascendente o descendente según los parámetros recibidos.
    """
    query = Cobro.query.join(Miembro).filter(
        Miembro.nombre.ilike(f"%{nombre_filtro}%"),
        Miembro.apellido.ilike(f"%{apellido_filtro}%"),
    )
    if medio_pago_filtro != "":
        medio_pago = MedioDePago(medio_pago_filtro).name
        query = query.filter(Cobro.medio_de_pago == medio_pago)

    if despues_de_filtro != "":
        query = query.filter(Cobro.fecha_pago >= despues_de_filtro)

    if antes_de_filtro != "":
        query = query.filter(Cobro.fecha_pago <= antes_de_filtro)

    if orden == "asc":
        query = query.order_by(getattr(Cobro, ordenar_por).asc())
    else:
        query = query.order_by(getattr(Cobro, ordenar_por).desc())

    cobros_ordenados = query.paginate(
        page=pagina, per_page=cant_por_pag, error_out=False
    )

    return cobros_ordenados


# función que crea un cobro
def crear_cobro(
    fecha_pago, medio_de_pago, monto, observaciones, joa_id, recibio_el_dinero_id
):
    """
    Funcion que crea un cobro.
    """
    cobro = Cobro(
        fecha_pago=fecha_pago,
        medio_de_pago=medio_de_pago,
        monto=monto,
        observaciones=observaciones,
        joa_id=joa_id,
        recibio_el_dinero_id=recibio_el_dinero_id,
    )
    db.session.add(cobro)
    db.session.commit()

    return cobro


def encontrar_cobro(id):
    """
    Funcion que busca un cobro a partir de su id y lo retorna, o retorna 404 si es un id que no se corresponde con un registro en la tabla.
    """
    return db.get_or_404(Cobro, id)


def guardar_cambios():
    """
    Funcion que guarda los cambios en la base de datos.
    """
    db.session.commit()


def marcar_deuda(joa_id):
    """
    Funcion que crea modifica la tabla de jinetes y amazonas para marcar que tiene deuda.
    """
    jya = db.get_or_404(JineteOAmazona, joa_id)
    jya.tiene_deuda = True
    db.session.commit()


def cargar_joa_choices():
    """
    Funcion que devuelve los jinetes y amazonas del sistema.
    """
    return [
        (joa.id, joa.nombre + " " + joa.apellido)
        for joa in JineteOAmazona.query.order_by("nombre")
    ]


def cargar_miembro_activo_choices():
    """
    Funcion que devuelve los miembros del sistema.
    """
    return [
        (miembro.id, miembro.nombre + " " + miembro.apellido)
        for miembro in Miembro.query.filter(Miembro.activo.is_(True)).order_by("nombre")
    ]

def listar_medios_de_pago():
    """
    Funcion que devuelve los medios de pago del sistema.
    """
    return MedioDePago.listar()
