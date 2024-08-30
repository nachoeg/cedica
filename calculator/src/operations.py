def multiply(a, b):
    return (a * b)


def divide(a, b):
    if b == 0:
        raise ValueError("¡No se puede dividir por cero!")
    
    return a / b

def subtract(a, b):
    return a - b