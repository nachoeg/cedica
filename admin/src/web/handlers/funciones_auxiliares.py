def booleano_a_palabra(bool):
    """Devuelve 'No' si el valor pasado por parámetro es False,
    'Sí' si es verdadero.
    """
    return ['No', 'Sí'][bool]


def palabra_a_booleano(palabra):
    """Devuelve True si el valor pasado por parámetro es 'Sí',
    False si es 'No'.
    """
    dicc = {'Sí': True, 'No': False, '': ''}
    return dicc[palabra]


def fechahora_a_fecha(fechahora):
    """Devuelve la fecha del parámetro con formato
    '%d-%m-%Y'.
    """
    return fechahora.strftime('%d-%m-%Y')


def fechahora(fechahora):
    """Devuelve fecha y hora del parámetro con formato
    '%d-%m-%Y %H:%M'.
    """
    return fechahora.strftime('%d-%m-%Y %H:%M')
