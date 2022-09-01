# This is a sample Python script.
import Quine_McCluskey
import time

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
        start = time.time()
        array.sort()
        binary_array = Quine_McCluskey.to_binary(array)
        binary_array.sort()
        grouped_array = Quine_McCluskey.group_1s(binary_array)
        grouped_array.sort(key=lambda x: x[0])
        prime_implicants = Quine_McCluskey.prime_implicant_search(grouped_array)
        prime_implicants = Quine_McCluskey.remove_repeated(prime_implicants)
        essential_prime_implicants = Quine_McCluskey.essential_implicant_search(prime_implicants)
        terms = Quine_McCluskey.turn_boolean(essential_prime_implicants)
        Quine_McCluskey.boolean_equation(terms)
        finish = time.time()

        print("La ejecucion se hizo en: " + str(finish-start) + "segundos.")


