import numpy as np

def expand_histogram(channel, matriz):
    # Encontrar los valores mínimo y máximo en el canal
    # Búsqueda de X1
    X1 = 0
    for i in range(256):
        if channel[i][0] != 0:
            X1 = i
            break
    # Búsqueda de X2
    X2 = 255
    for i in range(255, -1, -1):
        if channel[i][0] != 0:
            X2 = i
            break
    print(X1)
    print(X2)
    # Si X1=0 y X2=255, no se necesita expandir el histograma
    if(X1==0 and X2==255):
        return matriz
    print("Pasaste la prueba, estimado")
    m = 255/(X2-X1)
    b = X1-(m*X2)

    #T(r)=m*r+b
    # Expansión del histograma
    expanded = {}
    for i in range(X1, X2 + 1):
       new_value = int(np.round(m * i + b))
       if(new_value!=i):
            expanded[i] = new_value
    # Convertir el diccionario a dos listas: claves y valores
    claves = np.array(list(expanded.keys()))
    mask = np.isin(matriz, claves)
    matriz[mask] = np.vectorize(expanded.get)(matriz[mask])

    return matriz
