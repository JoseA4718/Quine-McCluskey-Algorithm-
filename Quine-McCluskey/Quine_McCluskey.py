
#Paso 1. Función para convertir los mintérminos a números binarios

def to_binary (minterms):
    binaryArray = []
    Bits = len(format(minterms[-1],"b")) #Función format, cambia valores de formato, "b" es para binario.

    for minterm in minterms:
        min = format(minterm,"b")
        min = min.zfill(Bits) #Llena el bit de ceros a la izquierda por si no tienen el mismo largo de bits.
        binaryArray.append(min) #Añade el mintérmino binario al array.
    print("Paso 1: Mintérminos insertados a binario: " + str(binaryArray))
    group_1s(binaryArray)
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
    delete_grade(grouped_list)
    return grouped_list

#Paso 3. Funciones que revisan que solo difieran en 1 bit y pone X en los bits diferentes.

#Elimina el número que indica la cantidad de 1's al inicio de cada subarray.
def delete_grade(grouped_array):
    subdivs = len(grouped_array) # Número de subgrupos del array ordenado, cada grupo implica un subset de la cantidad de 1s.
    for minterm in range(subdivs):
        grouped_array[minterm].pop(0) # Para cada sublista del array, elimina la posición 0 (El indicador de cantidad de 1s.)
    bit_compare("10110", "10010")
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














