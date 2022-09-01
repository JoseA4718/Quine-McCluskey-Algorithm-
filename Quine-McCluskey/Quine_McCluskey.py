import Constants

#Paso 1. Función para convertir los mintérminos a números binarios

def to_binary (minterms):
    binaryArray = []
    Bits = len(format(minterms[-1],"b")) #Función format, cambia valores de formato, "b" es para binario.

    for minterm in minterms:
        min = format(minterm,"b")
        min = min.zfill(Bits) #Llena el bit de ceros a la izquierda por si no tienen el mismo largo de bits.
        binaryArray.append(min) #Añade el mintérmino binario al array.
    print("Paso 1: Mintérminos insertados a binario: " + str(binaryArray))
    return binaryArray

#Paso 2. Función que agrupa mintérminos por la cantidad de 1s que tienen en representación binaria.

def group_1s (minterm_array):
    grouped_list = []
    for minterm in minterm_array:
        n = 0  #Para cada mintermino en el array, se establece un contador para contar la cantidad de 1s.
        for dig_1 in minterm:
            if dig_1 == "1":  #Verifica cada dígito del numero binario y suma 1 a su contador por cada 1 que encuentra.
                n += 1
        if len(grouped_list) == 0:
            grouped_list.append([n, minterm]) #Si ya la lista de mintérminos está vacía, significa que todos los números fueron contados y añade una tupla con el mintérmino y su cantidad de 1s.
        else: #Caso contrario, si la lista no está vacía sigue revisando el resto de mintérminos.
            counter = 0
            for sublist in grouped_list:
                if sublist[0] == n:
                    sublist.append(minterm)
                    break
                counter += 1
                if len(grouped_list) == counter:
                    grouped_list.append([n, minterm])
                    break
    print("Paso 2: La lista agrupada por cantidad de 1s es la siguiente: " + str(grouped_list))
    return grouped_list

#Paso 3. Funciones que revisan que solo difieran en 1 bit y pone X en los bits diferentes.

#Elimina el número que indica la cantidad de 1's al inicio de cada subarray.
def delete_grade(grouped_array):
    subdivs = len(grouped_array) # Número de subgrupos del array ordenado, cada grupo implica un subset de la cantidad de 1s.
    for minterm in range(subdivs):
        grouped_array[minterm].pop(0) # Para cada sublista del array, elimina la posición 0 (El indicador de cantidad de 1s.)
    return grouped_array

def bit_compare (minterm1, minterm2):
    bit_diff = 0
    n_bits = len(minterm1)
    new_minterm = ""

    for bit in range(n_bits): #Compara cada bit entre ambos minterminos, el bit 0 con el 0, el 1 con el 1 y asi constantemente, si difieren suma 1 a la diferencia
        bit1 = minterm1[bit] # de bits.
        bit2 = minterm2[bit]
        if bit1 != bit2:
            bit_diff += 1
            new_minterm += "X" #Si son diferentes pone una X en lugar del bit
        else:
            new_minterm += bit1 #Si son iguales mantiene el mismo bit
    if bit_diff < 2:
        #Si la diferencia es 1 o 0 retorna True y el mintermino nuevo
        return True, new_minterm
    else:
        #Si la diferencia es mayor a 1 retorna False y el mintermino nuevo
        return False, new_minterm

def repeat_check (minterm): #Revisa los bits del numero binario y si hay una X es porque ya fue revisado.
    for bit in minterm:
        if bit == "X":
            return True
    return False

# Paso 4. Funciones para conseguir los implicantes primos.

def prime_implicant_search (grouped_array):

    grouped_array = delete_grade(grouped_array)
    subarray_quantity = len(grouped_array)-1
    implicants = []
    prime_implicants = []
    prime_implicant_candidates = []
    prime_implicant_check = []

    if subarray_quantity > 0:
        for counter1 in range(subarray_quantity):
            for minterm1 in grouped_array[counter1]:  #Counter 1 se inicia en 1 para no tomar en cuenta el grado de cada subarray
                for counter2, minterm2 in enumerate(grouped_array[counter1 + 1]):
                    one_bit_diff, new_minterm = bit_compare(minterm1, minterm2)  #Recibe True si solo cambian por 1 bit y devuelve el mintermino de la comparacion (Con X)
                    if one_bit_diff:
                        implicants.append(new_minterm)  # Si el mintermino solo varia en 1 bit, lo anade a la lista de implicantes.
                        if counter1 == subarray_quantity - 1:
                            if minterm2 in prime_implicant_candidates:  # si un mintermino difiere con un solo bit, este se borra de prime_implicant_candidates
                                prime_implicant_candidates.remove(minterm2)
                    else:
                        if counter1 == subarray_quantity - 1:  # En caso de que sea del ultimo subarray de la lista
                            if minterm2 not in prime_implicant_candidates:  # Revisa si el mintermino no esta en la lista
                                prime_implicant_candidates.append(minterm2)  # Se inserta ese mintermino en la lista de candidatos.

                    prime_implicant_check.append(one_bit_diff)

                for counter, check in enumerate(prime_implicant_check):  #Compureba si el implicante es primo o no.
                    # Calcular la longitud del segundo grupo.
                    if isinstance(grouped_array[counter1 + 1], str):
                        second_group_length = 0
                    else:
                        second_group_length = len(grouped_array[counter1 + 1]) - 1
                    if check: #Si el mintermino se pudo emparejar sale del for
                        break
                    elif not check and counter == len(prime_implicant_check) - 1 and counter2 == second_group_length and not repeat_check(minterm1):
                        prime_implicants.append(minterm1)  # Al no poderse emparejar con otro mintermino, se anade a los implicantes primos
                    elif not check and counter == len(prime_implicant_check) - 1 and repeat_check(minterm1):
                        prime_implicants.append(minterm1)  # Al no poderse emparejar con otro mintermino, se anade a los implicantes primos

                prime_implicant_check = []

        implicant_groups = group_1s(implicants) #Crea el grupo de implicantes a partir de la agrupacion por la cantidad de 1s
        prime_implicants += prime_implicant_search(implicant_groups)
        if prime_implicant_candidates: #Si no esta vacia
            for implicant in prime_implicant_candidates:
                prime_implicants.append(implicant)
        if prime_implicants == [] and counter1 == subarray_quantity - 1:  #Si no se pudo combinar uno de los minterminos
            for group in grouped_array:
                for minterm in group:
                    prime_implicants.append(minterm)  # Almacena los minterminos como implicantes primos
    elif subarray_quantity == 0:  #En caso de que la lista tenga un solo subarray
        for implicant in grouped_array[0]:
            prime_implicants.append(implicant)
    print("Paso 3: La lista de implicantes primos es la siguiente: " + str(prime_implicants))
    return prime_implicants

#Revisa si hay elementos repetidos dentro de la lista, de ser asi los elimina
#Esto para reducir al maximo la expresion y no tener expresiones iguales al final
def remove_repeated (array):
    for element in array:
        quantity = array.count(element)
        while quantity > 1:
            array.remove(element)
            quantity -= 1
    print("Los implicantes primos con los valores repetidos eliminados es: " + str(array))
    return array


#Funcion que encuentra los minterminos que conforman a los minterminos con valor de "no importa" (X).
def minterm_search(minterm): #Los minterminos se almacenan en su forma decimal.
    x_count = minterm.count('X') #Cuenta la cantidad de X's en el mintermino.
    if x_count == 0:
        return [int(minterm, 2)] #Retorna el mintermino en decimal
    x = [bin(i)[2:].zfill(x_count) for i in range(pow(2, x_count))] #Define x como el binario del corte desde la posicion 2, para los valores de 2 a la cantidad de X.
    minterms = []

    for i in range(pow(2, x_count)):
        minterms_aux, index = minterm[:], -1
        for j in x[0]:
            if index != -1:
                ind = index + minterms_aux[index + 1:].find('X') + 1
            else:
                ind = minterms_aux[index + 1:].find('X')
            minterms_aux = minterms_aux[:ind] + j + minterms_aux[ind + 1:]
        minterms.append(int(minterms_aux, 2))
        x.pop(0)

    return minterms


# Función que encuentra los implicantes primos esenciales a partir del array de implicantes primos
def essential_implicant_search(prime_implicants):
    essential_implicants = []
    implicants = []  #Guarda una lista de los minterminos relacionados con su mintermino primo.
    prime_implicant_check = []  #Valor boolano, True si el mintermino no se repite, False si se repite.
    limit = 0  #Limite de control de los grupos, para no exederse a la hora de revisar n grupos.

    for minterm in prime_implicants:
        minterms = minterm_search(minterm)
        implicants.append(minterms) #Llama a minterm_search y obtiene los minerminos que conforman el mintermino compuesto.

    implicant_quantity = len(implicants) - 1  #Valor de la cantidad de implicantes primos -1 (El -1 es para control)

    if implicant_quantity > 0:  # Si la lista posee dos o más implicantes primos
        for counter1 in range(implicant_quantity + 1):
            if counter1 != implicant_quantity:  #Revisa que el mintermino no este en la subarray del final.
                for min1 in implicants[counter1]:
                    for counter2 in range(1, len(implicants) - limit):
                        for min2 in implicants[counter1 + counter2]:
                            if min1 == min2:
                                prime_implicant_check.append(False)
                                break
                            else:
                                prime_implicant_check.append(True)

                    for counter, check in enumerate(prime_implicant_check):  #Revisa si el implicante es esencial o no.
                        if not check:
                            break # Si no lo es, hace break
                        elif check and counter == len(prime_implicant_check) - 1:
                            if prime_implicants[counter1] not in essential_implicants:
                                essential_implicants.append(prime_implicants[counter1])  #Caso en que el mintermino no se repite, por lo que se anade a la lista de esenciales

                    prime_implicant_check = []
                limit += 1

            else:  # Caso final donde solo queda revisar el ultimo grupo.
                reversed_implicants = list(reversed(implicants))  #Se invierte la lista para poder comparar los minterminos.
                reversed_prime_implicants = list(reversed(prime_implicants))  # Se invierte la lista de implicantes primos igualmente.

                for minterm1 in reversed_implicants[0]:
                    if reversed_prime_implicants[0] not in essential_implicants:
                        for counter2 in range(1, len(implicants)):
                            for minterm2 in reversed_implicants[counter2]:
                                if minterm1 == minterm2:
                                    prime_implicant_check.append(False)
                                    break
                                else:
                                    prime_implicant_check.append(True)

                        for counter, response in enumerate(prime_implicant_check):  # Comprobar si el elemento es un implicante esencial o no.
                            if not response:
                                break
                            elif response and counter == len(prime_implicant_check) - 1:
                                essential_implicants.append(reversed_prime_implicants[0])  # Añadir el mintermino a los implicantes esenciales dado que posee un mintermino que no se repite.

                        prime_implicant_check = []

    elif implicant_quantity == 0:  #En caso de que haya solo un implicante primo
        essential_implicants.append(prime_implicants[0])
    print("Los implicantes primos esenciales son los siguientes: " + str(essential_implicants))
    return essential_implicants

#Función que convierte a la expresion booleana
def turn_boolean(values):
    list = []
    for term in values:
        variable = " "
        for x in range(len(term)): #Revisa el valor del implicante
            if term[x] == "X": #Si se encuentra una X la ignora y sigue revisando, y pone el valor del literal en cada posicion
                continue
            variable += Constants.literals[x]
            if term[x] == "0": #En caso de encontrarse un 0, significa que esta negado, por lo que le anade una comilla para representar negacion
                variable += "'"
        list.append(variable)
    return list

#Función que representa la la lista de expresiones booleanas como una ecuacion booleana
def boolean_equation(list):
    string = "Y = "
    for element in list:
        string += element + " + " #Concatena los elementos dentro del string con un mas
    print("La ecuacion booleana de los minterminos dados es: " + string[:len(string)-3])













