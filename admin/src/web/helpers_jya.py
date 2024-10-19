from flask import current_app


def archivo_url(archivo):
    cliente = current_app.storage.client

    if archivo is None:
        return ""
    
    return cliente.presigned_get_object("grupo17", archivo)

