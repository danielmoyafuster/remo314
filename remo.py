
# ---------------------------------------------------------------------------------------------------------
# OBTENER DICCIONARIO DE PUERTOS Y COORDENADAS -> POBLACIÓN (CODIGOS DE MUNICIPIOS)
# --------------------------------------------------------------------------------------------------------- 
import requests
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time
import unidecode
import streamlit as st
import json
import folium
from streamlit_folium import folium_static
from geopy.distance import geodesic
from streamlit_folium import st_folium
# ---------------------------------------------------------------------------------------------------------
# API Key de AEMET
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJkYW5pZWxtb3lhZnVzdGVyQGdtYWlsLmNvbSIsImp0aSI6ImE5YzRlYzA2LTQ5ZmMtNGIyZi04OGU4LWRjNTQ1MDA1MThmYiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNzQwNjY4MjQ4LCJ1c2VySWQiOiJhOWM0ZWMwNi00OWZjLTRiMmYtODhlOC1kYzU0NTAwNTE4ZmIiLCJyb2xlIjoiIn0.FPSuXda0P6PeRFZ80LHCW-O6cMdMR8RLTFl_pBKQ6q4"
# ---------------------------------------------------------------------------------------------------------
# DICCIONARIO PUERTOS -> CODIGOS DE MUNICIPIOS -> COORDENADAS GPS -> SUBZONA PORTUARIA
# ---------------------------------------------------------------------------------------------------------
datos_puertos = {
    "Puerto de Alicante": ("03014", (38.3452, -0.4810), "Aguas costeras de Alicante"),
    "Puerto de Altea": ("03018", (38.5986, -0.0515), "Aguas costeras de Alicante"),
    "Puerto de Benidorm": ("03031", (38.5342, -0.1310), "Aguas costeras de Alicante"),
    "Puerto de Burriana": ("12032", (39.8895, -0.0847), "Aguas costeras de Castellón"),
    "Puerto de Calpe": ("03047", (38.6445, 0.0673), "Aguas costeras de Alicante"),
    "Puerto de Castellón": ("12040", (39.9689, -0.0226), "Aguas costeras de Castellón"),
    "Puerto de Cullera": ("46105", (39.1641, -0.2510), "Aguas costeras de Valencia"),
    "Puerto de Dénia": ("03063", (38.8408, 0.1057), "Aguas costeras de Alicante"),
    "Puerto de El Campello": ("03050", (38.4285, -0.3991), "Aguas costeras de Alicante"),
    "Puerto de Gandía": ("46131", (38.9955, -0.1602), "Aguas costeras de Valencia"),
    "Puerto de Guardamar del Segura": ("03076", (38.0897, -0.6500), "Aguas costeras de Alicante"),
    "Puerto de Jávea": ("03082", (38.7939, 0.1805), "Aguas costeras de Alicante"),
    "Puerto de Marina Benidorm": ("03031", (38.5342, -0.1310), "Aguas costeras de Alicante"),
    "Puerto de Marina Burriana": ("12032", (39.8895, -0.0847), "Aguas costeras de Castellón"),
    "Puerto de Marina Calpe": ("03047", (38.6445, 0.0673), "Aguas costeras de Alicante"),
    "Puerto de Marina Cullera": ("46105", (39.1641, -0.2510), "Aguas costeras de Valencia"),
    "Puerto de Marina Dénia": ("03063", (38.8408, 0.1057), "Aguas costeras de Alicante"),
    "Puerto de Marina Jávea": ("03082", (38.7939, 0.1805), "Aguas costeras de Alicante"),
    "Puerto de Marina Moraira": ("03047", (38.6880, 0.1453), "Aguas costeras de Alicante"),
    "Puerto de Marina Oliva": ("06093", (38.9190, -0.1198), "Aguas costeras de Valencia"),
    "Puerto de Marina Oropesa": ("12085", (40.0964, 0.1430), "Aguas costeras de Castellón"),
    "Puerto de Marina Peñíscola": ("12089", (40.3597, 0.4061), "Aguas costeras de Castellón"),
    "Puerto de Marina Real Juan Carlos I": ("06139", (39.4538, -0.3236), "Aguas costeras de Valencia"),
    "Puerto de Marina Santa Pola": ("03121", (38.1913, -0.5663), "Aguas costeras de Alicante"),
    "Puerto de Marina Torrevieja": ("03133", (37.9774, -0.6804), "Aguas costeras de Alicante"),
    "Puerto de Marina Valencia": ("06139", (39.4538, -0.3236), "Aguas costeras de Valencia"),
    "Puerto de Marina Vinaroz": ("12138", (40.4700, 0.4753), "Aguas costeras de Castellón"),
    "Puerto de Marina Greenwich": ("03047", (38.6346, 0.0703), "Aguas costeras de Alicante"),
    "Puerto de Moraira": ("03047", (38.6880, 0.1453), "Aguas costeras de Alicante"),
    "Puerto de Oliva": ("06093", (38.9190, -0.1198), "Aguas costeras de Valencia"),
    "Puerto de Oropesa": ("12085", (40.0964, 0.1430), "Aguas costeras de Castellón"),
    "Puerto de Peñíscola": ("12089", (40.3597, 0.4061), "Aguas costeras de Castellón"),
    "Puerto de Pilar de la Horadada": ("03902", (37.8670, -0.7900), "Aguas costeras de Alicante"),
    "Puerto de Santa Pola": ("03121", (38.1913, -0.5663), "Aguas costeras de Alicante"),
    "Puerto de Sagunto": ("46220", (39.6447, -0.2389), "Aguas costeras de Valencia"),
    "Puerto de Torrevieja": ("03133", (37.9774, -0.6804), "Aguas costeras de Alicante"),
    "Puerto de Valencia": ("06139", (39.4538, -0.3236), "Aguas costeras de Valencia"),
    "Puerto de Vinaroz": ("12138", (40.4700, 0.4753), "Aguas costeras de Castellón"),
    "Puerto de Villajoyosa": ("03139", (38.5070, -0.2324), "Aguas costeras de Alicante")
}

# ---------------------------------------------------------------------------------------------------------
# FUNCIONES PARA OBTENER DATOS DE AEMET
# ---------------------------------------------------------------------------------------------------------
# 🔹 Función para obtener predicción meteorológica
def obtener_prediccion(codigo_municipio):
    url_prediccion = f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/{codigo_municipio}/"
    params = {"api_key": API_KEY}

    response = requests.get(url_prediccion, params=params)
    if response.status_code == 200:
        data_json = response.json()
        if "datos" in data_json:
            data_url = data_json["datos"]
            data_response = requests.get(data_url)
            return data_response.json() if data_response.status_code == 200 else None
    return None

# 🔹 Función para obtener estado del mar
def obtener_estado_mar():
    url_mar = "https://opendata.aemet.es/opendata/api/prediccion/maritima/costera/costa/46/"
    params = {"api_key": API_KEY}

    response = requests.get(url_mar, params=params)
    if response.status_code == 200:
        data_json_mar = response.json()
        if "datos" in data_json_mar:
            data_url_mar = data_json_mar["datos"]
            data_response_mar = requests.get(data_url_mar)
            return data_response_mar.json() if data_response_mar.status_code == 200 else None
    return None

# 🔹 Función para estimar altura de olas, periodo y estado del mar basado en viento
def estimar_estado_mar(velocidad_viento, fetch=10):
    """
    Calcula la altura de las olas, el periodo y el estado del mar basado en el viento.
    :param velocidad_viento: Velocidad del viento en m/s
    :param fetch: Distancia recorrida por el viento sobre el agua en km (por defecto 10 km)
    :return: (altura_olas, periodo_olas, estado_mar)
    """
    
    if velocidad_viento > 20:  # Asumimos que el dato está en km/h si es grande
        velocidad_viento = velocidad_viento / 3.6  # Convertir km/h a m/s
    
    altura_olas = 0.0245 * (velocidad_viento ** 1.2) * (fetch ** 0.3)
    periodo_olas = 0.67 * (altura_olas ** 0.5)

    if altura_olas < 0.1:
        estado_mar = "Mar en calma"
    elif altura_olas < 0.5:
        estado_mar = "Mar rizada"
    elif altura_olas < 1.25:
        estado_mar = "Marejadilla"
    elif altura_olas < 2.5:
        estado_mar = "Marejada"
    elif altura_olas < 4.0:
        estado_mar = "Fuerte marejada"
    elif altura_olas < 6.0:
        estado_mar = "Gruesa"
    elif altura_olas < 9.0:
        estado_mar = "Muy gruesa"
    elif altura_olas < 14.0:
        estado_mar = "Arbolada"
    else:
        estado_mar = "Montañosa"

    return round(altura_olas, 2), round(periodo_olas, 2), estado_mar

# 🔹 Interfaz en Streamlit
st.title("🌊 Predicción Meteorológica en Puertos de la Comunidad Valenciana")

# 📌 Selección del puerto
puerto_seleccionado = st.selectbox("Selecciona un puerto:", list(datos_puertos.keys()))
codigo_municipio, coordenadas, subzona = datos_puertos[puerto_seleccionado]

# 🔹 Mapa interactivo
st.subheader("🗺️ Ubicación en el mapa")
mapa = folium.Map(location=coordenadas, zoom_start=10)
folium.Marker(location=coordenadas, popup=f"{puerto_seleccionado}", icon=folium.Icon(color="blue", icon="info-sign")).add_to(mapa)
folium_static(mapa)

# 🔹 Obtener y mostrar predicción meteorológica
datos_prediccion = obtener_prediccion(codigo_municipio)
if datos_prediccion:
    prediccion_hoy = datos_prediccion[0]["prediccion"]["dia"][0]
    prediccion_manana = datos_prediccion[0]["prediccion"]["dia"][1]

    estado_cielo_hoy = next((e["descripcion"] for e in prediccion_hoy["estadoCielo"] if e["periodo"] == "12-24"), "No disponible")
    estado_cielo_manana = next((e["descripcion"] for e in prediccion_manana["estadoCielo"] if e["periodo"] == "12-24"), "No disponible")

    fecha_hoy = prediccion_hoy["fecha"][:10]
    fecha_manana = prediccion_manana["fecha"][:10]

    st.subheader(f"📡 Predicción para {puerto_seleccionado}")
    st.write(f"📅 **Hoy ({fecha_hoy}):** {estado_cielo_hoy}, 🌡 Temp. Máx: {prediccion_hoy['temperatura']['maxima']}°C, Temp. Mín: {prediccion_hoy['temperatura']['minima']}°C")
    st.write(f"📅 **Mañana ({fecha_manana}):** {estado_cielo_manana}, 🌡 Temp. Máx: {prediccion_manana['temperatura']['maxima']}°C, Temp. Mín: {prediccion_manana['temperatura']['minima']}°C")

# 🔹 Obtener y mostrar estado del mar
datos_mar_json = obtener_estado_mar()
if datos_mar_json:
    for zona in datos_mar_json[0]["prediccion"]["zona"]:
        if zona["nombre"] == subzona:
            st.subheader(f"🌊 Estado del Mar en {subzona}")
            for subzona_data in zona["subzona"]:
                st.write(f"📍 **{subzona_data['nombre']}**")
                st.write(f"🌊 **Descripción:** {subzona_data['texto']}")
                st.write("---")
            break

# 🔹 Calcular y mostrar estado estimado del mar basado en viento
velocidad_viento = 30  # Sustituir por el dato real
altura_olas, periodo_olas, estado_mar = estimar_estado_mar(velocidad_viento)
st.subheader("🌊 Estado Estimado del Mar")
st.write(f"🌊 **Altura de las Olas:** {altura_olas} m")
st.write(f"⏳ **Periodo de las Olas:** {periodo_olas} s")
st.write(f"📌 **Estado del Mar:** {estado_mar}")