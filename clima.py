import json
import time  # NUEVO: Para manejar el tiempo de expiración
import urllib.error
import urllib.parse
import urllib.request

try:
    from flask import Flask, render_template, request, jsonify
except ImportError as e:
    raise ImportError(
        "Flask no está instalado. Instálalo con 'pip install flask' e intenta de nuevo."
    ) from e

app = Flask(__name__)

# Configuración de funcionalidad avanzada: Caché en memoria con TTL
# Estructura: { "ciudad": {"data": dict, "expires_at": float} }
CACHE = {}
CACHE_TTL = 300  # Tiempo de vida de la caché: 5 minutos (300 segundos)


def obtener_coordenadas(ciudad):
    """Traduce el nombre de una ciudad a coordenadas usando el buscador de Open-Meteo."""
    url = (
        "https://geocoding-api.open-meteo.com/v1/search"
        f"?name={urllib.parse.quote(ciudad)}&count=1&language=es&format=json"
    )
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            datos = json.load(response)
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        raise ConnectionError(
            "Error de comunicación con el servicio de geocodificación."
        ) from e

    if not datos.get("results"):
        raise ValueError("Ciudad no encontrada")

    resultado = datos["results"][0]
    return resultado["latitude"], resultado["longitude"], resultado["name"]


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/clima", methods=["GET"])
def obtener_clima():
    ciudad = request.args.get("ciudad", "").strip().lower()

    if not ciudad:
        return jsonify({"error": "Por favor, ingresa una ciudad válida."}), 400

    now = time.time()
    cached = CACHE.get(ciudad)

    # 1. VERIFICACIÓN: Si está en caché y sigue siendo válida, devolver de inmediato
    if cached and now < cached["expires_at"]:
        print(f"[Cache Hit] Sirviendo datos válidos para: {ciudad}")
        return jsonify(cached["data"])

    try:
        # 2. SOLICITUD A LAS APIs (Si no hay caché o ya expiró)
        # Paso A: Obtener Coordenadas
        lat, lon, nombre_oficial = obtener_coordenadas(ciudad)

        # Paso B: Llamada a la API de Clima
        url_clima = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            "&daily=weathercode,temperature_2m_max,temperature_2m_min&timezone=auto"
        )

        try:
            with urllib.request.urlopen(url_clima, timeout=5) as response:
                datos_clima = json.load(response)
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            raise ConnectionError(
                "Error de comunicación con el servicio del clima."
            ) from e

        daily = datos_clima["daily"]

        # Estructurar la respuesta
        pronostico = []
        for i in range(3):
            pronostico.append(
                {
                    "fecha": daily["time"][i],
                    "max": daily["temperature_2m_max"][i],
                    "min": daily["temperature_2m_min"][i],
                    "codigo": daily["weathercode"][i],
                }
            )

        resultado_final = {"ciudad": nombre_oficial, "pronostico": pronostico}

        # Guardar en caché con su tiempo futuro de expiración
        CACHE[ciudad] = {"data": resultado_final, "expires_at": now + CACHE_TTL}

        print(f"[API Success] Datos guardados en caché para: {ciudad}")
        return jsonify(resultado_final)

    # 3. MANEJO DE ERRORES: Tolerancia a fallos con datos expirados
    except ValueError as ve:
        # Si la ciudad no existe, no tiene sentido usar caché vieja
        return jsonify({"error": str(ve)}), 404

    except (ConnectionError, Exception) as e:
        print(f"[Error de Red/Servidor]: {str(e)}")

        # Si la API falla pero tenemos datos viejos en caché, los devolvemos
        if cached:
            print(
                f"[Cache Fallback] La API falló. Devolviendo caché expirada para: {ciudad}"
            )
            # Opcional: Puedes agregar una bandera para avisar al cliente que el dato es viejo
            resultado_viejo = cached["data"].copy()
            resultado_viejo["cached_fallback"] = True
            return jsonify(resultado_viejo)

        # Si no hay API ni registros previos en caché, mostramos el error original
        if isinstance(e, ConnectionError):
            return (
                jsonify(
                    {
                        "error": "Error de comunicación con el servicio del clima. Intenta más tarde."
                    }
                ),
                503,
            )
        return jsonify({"error": "Ocurrió un error inesperado en el servidor."}), 500


if __name__ == "__main__":
    app.run(debug=True)
