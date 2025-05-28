# tsp_solver.py
import math
import random

def distancia(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def evalua_ruta(ruta, coord):
    total = 0
    for i in range(len(ruta)-1):
        total += distancia(coord[ruta[i]], coord[ruta[i+1]])
    total += distancia(coord[ruta[-1]], coord[ruta[0]])
    return total

def busqueda_tabu(ruta_inicial, coord, iteraciones=1000, tamaño_tabu=10):
    mejor_estado = ruta_inicial[:]
    estado_actual = ruta_inicial[:]
    mejor_valor = evalua_ruta(mejor_estado, coord)
    memoria_tabu = []
    persistencia = {}

    while iteraciones > 0:
        iteraciones -= 1
        vecinos = []

        for i in range(1, len(estado_actual) - 1):
            for j in range(i+1, len(estado_actual) - 1):
                vecino = estado_actual[:]
                vecino[i], vecino[j] = vecino[j], vecino[i]
                vecinos.append(vecino)

        vecinos_ordenados = sorted(vecinos, key=lambda x: evalua_ruta(x, coord))

        for vecino in vecinos_ordenados:
            cambio = tuple(vecino)

            if cambio not in memoria_tabu:
                valor_vecino = evalua_ruta(vecino, coord)
                valor_actual = evalua_ruta(estado_actual, coord)

                if valor_vecino < valor_actual:
                    estado_actual = vecino[:]
                    memoria_tabu.append(cambio)
                    persistencia[cambio] = 5

                    if valor_vecino < mejor_valor:
                        mejor_estado = vecino[:]
                        mejor_valor = valor_vecino
                    break
                elif valor_vecino < mejor_valor:
                    estado_actual = vecino[:]
                    memoria_tabu.append(cambio)
                    mejor_estado = vecino[:]
                    mejor_valor = valor_vecino
                    persistencia[cambio] = 5
                    break

        # Disminuir persistencia
        for cambio in list(persistencia):
            persistencia[cambio] -= 1
            if persistencia[cambio] <= 0:
                persistencia.pop(cambio)
                memoria_tabu.remove(cambio)

    return mejor_estado
