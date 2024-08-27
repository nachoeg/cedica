from src import calculator


def main():
    num1 = float(input("Escribe el primer numero:  "))
    operator = input("Escribe el operador (+, -, *, /):  ")
    num2 = float(input("Escribe el segundo numero:  "))
    result = calculator.calculate(num1, operator, num2)
    print(f"El resultado es: {result}")


if __name__ == "__main__":
    main()
