from src.core.database import db
from src.core.jinetes_y_amazonas.jinetes_y_amazonas import JineteOAmazona, Diagnostico

# funcion que crea un diagnóstico médico
def crear_diagnostico(**kwargs):
    diagnostico = Diagnostico(**kwargs)
    db.session.add(diagnostico)
    db.session.commit()

    return diagnostico

# funcion que lista todos los jinetes o amazonas del sistema
def listar_j_y_a(orden_asc=1, pagina_inicial=1, por_pag=20):
    j_y_a = JineteOAmazona.todos_paginados(orden_asc, pagina_inicial,por_pag)
    
    return j_y_a


# función que crea un registro de jinete o amazona
def crear_j_o_a(**kwargs):
    j_o_a = JineteOAmazona(**kwargs)
    db.session.add(j_o_a)
    db.session.commit()

    return j_o_a