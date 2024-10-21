def booleano_a_palabra(bool):
    return ['No', 'Sí'][bool]


def fechahora_a_fecha(fechahora):
    return fechahora.strftime('%d-%m-%Y')


def fechahora(fechahora):
    return fechahora.strftime('%d-%m-%Y %H:%M')