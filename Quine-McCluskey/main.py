# This is a sample Python script.
import Quine_McCluskey

if __name__ == '__main__':
    print("|Algoritmo de Quine-McCluskey|")
    print("Inserte el número de variables:")
    var = int(input())
    x = 0
    array = []

    while x != var:
        print("Inserte el valor de uno de los mintérminos")
        array.append(int(input()))
        x += 1

    if var != x:
        print("Los minterminos puestos no son la misma cantidad ingresada al inicio")

    else:
        Quine_McCluskey.ToBinary(array)

