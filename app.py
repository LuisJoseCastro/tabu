from tabu import busqueda_tabu, evalua_ruta
from flask import Flask, render_template, request
import math
import random

app = Flask(__name__)

# Coordenadas de ciudades
coord = {
    'Jiloyork' :(19.916012, -99.580580),
    'Toluca':(19.289165, -99.655697),
    'Atlacomulco':(19.799520, -99.873844),
    'Guadalajara':(20.677754472859146, -103.34625354877137),
    'Monterrey':(25.69161110159454, -100.321838480256),
    'QuintanaRoo':(21.163111924844458, -86.80231502121464),
    'Michoacan':(19.701400113725654, -101.20829680213464),
    'Aguascalientes':(21.87641043660486, -102.26438663286967),
    'CDMX':(19.432713075976878, -99.13318344772986),
    'QRO':(20.59719437542255, -100.38667040246602)
}

def distancia(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)


def simulated_annealing(ruta, T, T_MIN, V_enfriamiento):
    while T > T_MIN:
        dist_actual = evalua_ruta(ruta)
        for _ in range(int(V_enfriamiento)):
            i = random.randint(0, len(ruta)-1)
            j = random.randint(0, len(ruta)-1)
            ruta_tmp = ruta[:]
            ruta_tmp[i], ruta_tmp[j] = ruta_tmp[j], ruta_tmp[i]
            dist = evalua_ruta(ruta_tmp)
            delta = dist_actual - dist
            if dist < dist_actual or random.random() < math.exp(delta / T):
                ruta = ruta_tmp[:]
                dist_actual = dist
        T -= 0.005
    return ruta

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/resolver", methods=["POST"])
def resolver():
    try:
        origen = request.form["origen"]
        destino = request.form["destino"]

        # Crear ruta inicial
        ciudades_restantes = [c for c in coord if c != origen and c != destino]
        ruta = [origen] + ciudades_restantes + [destino]

        # Ejecutar búsqueda tabú con las coordenadas actuales
        ruta_optima = busqueda_tabu(ruta, coord)
        distancia_total = evalua_ruta(ruta_optima, coord)

        return render_template("index.html", ruta=ruta_optima, distancia=round(distancia_total, 4))
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    app.run(debug=True)