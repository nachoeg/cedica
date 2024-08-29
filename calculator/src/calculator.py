from src import operations


def calculate(a, operator, b):
    if operator == "+":
        # return operations.add(a, b)
        return "No esta implementada la suma"
    elif operator == "-":
        # return operations.subtract(a, b)
        return "No esta implementada la resta"
    elif operator == "*":
        return operations.multiply(a, b)
    elif operator == "/":
        # return operations.divide(a, b)
        return "No esta implementada la division"
    else:
        return ValueError(f"Operador no valido: {operator}")
