
#Función para convertir los mintérminos a números binarios

def ToBinary (minterms):
    binaryArray = []
    Bits = len(format(minterms[-1],"b"))

    for minterm in minterms:
        min = format(minterm,"b")
        min = min.zfill(Bits)
        binaryArray.append(min)
    print("Mintérminos insertados a binario: " + str(binaryArray))
    return binaryArray



