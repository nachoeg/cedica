from src.core.database import db
from src.core.anuncios.anuncio import Anuncio, Estado


def crear_anuncio(titulo, copete, contenido, autor_id, estado="bo"):
    """Crea un objeto de tipo Anuncio con los datos que recibe por
    parámetro y lo devuelve.
    """
    anuncio = Anuncio(titulo=titulo, copete=copete, contenido=contenido,
                      autor_id=autor_id, estado=estado)
    db.session.add(anuncio)
    db.session.commit()

    return anuncio


def listar_anuncios(
        titulo_filtro="",
        autor_filtro="",
        estado_filtro="",
        despues_de_filtro="",
        antes_de_filtro="",
        ordenar_por="id",
        orden="asc",
        pagina=1,
        cant_por_pag=6,
):
    """
    Lista todos los anuncios del sistema.
    Recibe como parámetros filtros que ingresa
    el usuario y devuelve los anuncios ordenados por id
    en orden ascendente o descendente según los
    parámetros recibidos.
    """

    query = Anuncio.query.filter(
        Anuncio.titulo.ilike(f"%{titulo_filtro}%"),
    )

    if estado_filtro != "":
        estado = Estado(estado_filtro).name
        query = query.filter(Anuncio.estado == estado)

    if despues_de_filtro != "":
        query = query.filter(Anuncio.fecha_publicacion >= despues_de_filtro)

    if antes_de_filtro != "":
        query = query.filter(Anuncio.fecha_publicacion <= antes_de_filtro)

    cant_resultados = query.count()

    if orden == "asc":
        query = query.order_by(getattr(Anuncio, ordenar_por).asc())
    else:
        query = query.order_by(getattr(Anuncio, ordenar_por).desc())

    anuncios = query.paginate(
        page=pagina, per_page=cant_por_pag, error_out=False
    )
    return anuncios, cant_resultados

def listar_anuncios_api(
        autor_filtro="",
        despues_de_filtro="",
        antes_de_filtro="",
        pagina=1,
        cant_por_pag=6,
):
    """
    Lista todos los anuncios del sistema.
    Recibe como parámetros filtros que ingresa
    el usuario y devuelve los anuncios ordenados por id
    en orden ascendente o descendente según los
    parámetros recibidos.
    """

    query = Anuncio.query.filter(
        Anuncio.titulo.ilike(f"%{autor_filtro}%"),
    )

    if despues_de_filtro != "":
        query = query.filter(Anuncio.fecha_publicacion >= despues_de_filtro)

    if antes_de_filtro != "":
        query = query.filter(Anuncio.fecha_publicacion <= antes_de_filtro)

    cant_resultados = query.count()
    
    anuncios = query.paginate(
        page=pagina, per_page=cant_por_pag, error_out=False
    )
    return anuncios, cant_resultados

def encontrar_anuncio(id):
    """
    Función que retorna un anuncio
    dado el id
    """
    anuncio = Anuncio.query.get_or_404(id)

    return anuncio


def eliminar_anuncio(id):
    """
    Funcion que elimina un anuncio
    dado el id del mismo.
    """
    anuncio = Anuncio.query.get_or_404(id)
    db.session.delete(anuncio)
    db.session.commit()


def guardar_cambios():
    """
    Función que persiste los cambios.
    """
    db.session.commit()

def listar_estados():
    """
    Función que devuelve los estados de un anuncio.
    """
    return Estado.listar()