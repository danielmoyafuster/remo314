import requests
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import folium_static
from geopy.distance import geodesic

# API Key de AEMET (sustituye con la tuya)
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJkYW5pZWxtb3lhZnVzdGVyQGdtYWlsLmNvbSIsImp0aSI6ImE5YzRlYzA2LTQ5ZmMtNGIyZi04OGU4LWRjNTQ1MDA1MThmYiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNzQwNjY4MjQ4LCJ1c2VySWQiOiJhOWM0ZWMwNi00OWZjLTRiMmYtODhlOC1kYzU0NTAwNTE4ZmIiLCJyb2xlIjoiIn0.FPSuXda0P6PeRFZ80LHCW-O6cMdMR8RLTFl_pBKQ6q4"

# URL de AEMET para obtener todas las estaciones climatológicas
url_estaciones = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones/"


# Diccionario de puertos con sus coordenadas
# (Este es un ejemplo; deberás completar con todos los puertos recopilados)
puertos = {
    "Puerto de Valencia": (39.4538, -0.3236),
    "Puerto de Alicante": (38.3452, -0.4810),
    "Puerto de Castellón": (39.9689, -0.0226),
    "Puerto de Gandía": (38.9955, -0.1602),
    "Puerto de Dénia": (38.8408, 0.1057),
    "Puerto de Sagunto": (39.6447, -0.2389),
    "Puerto de Torrevieja": (37.9774, -0.6804),
    "Puerto de Altea": (38.5986, -0.0515),
    "Puerto de Benidorm": (38.5342, -0.1310),
    "Puerto de Calpe": (38.6445, 0.0673),
    "Puerto de Santa Pola": (38.1913, -0.5663),
    "Puerto de Villajoyosa": (38.5070, -0.2324),
    "Puerto de Burriana": (39.8895, -0.0847),
    "Puerto de Peñíscola": (40.3597, 0.4061),
    "Puerto de Vinaroz": (40.4700, 0.4753),
    "Puerto de Oropesa": (40.0964, 0.1430),
    "Puerto de Jávea": (38.7939, 0.1805),
    "Puerto de Moraira": (38.6880, 0.1453),
    "Puerto de Cullera": (39.1641, -0.2510),
    "Puerto de Oliva": (38.9190, -0.1198),
    "Puerto de El Campello": (38.4285, -0.3991),
    "Puerto de Pilar de la Horadada": (37.8670, -0.7900),
    "Puerto de Guardamar del Segura": (38.0897, -0.6500),
    "Puerto de Marina Greenwich": (38.6346, 0.0703),
    "Puerto de Marina de Valencia": (39.4538, -0.3236),
    "Puerto de Marina Real Juan Carlos I": (39.4538, -0.3236),
    "Puerto de Marina Dénia": (38.8408, 0.1057),
    "Puerto de Marina Torrevieja": (37.9774, -0.6804),
    "Puerto de Marina Benidorm": (38.5342, -0.1310),
    "Puerto de Marina Calpe": (38.6445, 0.0673),
    "Puerto de Marina Santa Pola": (38.1913, -0.5663),
    "Puerto de Marina Burriana": (39.8895, -0.0847),
    "Puerto de Marina Peñíscola": (40.3597, 0.4061),
    "Puerto de Marina Vinaroz": (40.4700, 0.4753),
    "Puerto de Marina Oropesa": (40.0964, 0.1430),
    "Puerto de Marina Jávea": (38.7939, 0.1805),
    "Puerto de Marina Moraira": (38.6880, 0.1453),
    "Puerto de Marina Cullera": (39.1641, -0.2510),
    "Puerto de Marina Oliva": (38.9190, -0.1198)
}
#
# --------------------------------------------------------------------------------------------------------------
#

# 🔹 Obtener estaciones meteorológicas 🔹
try:
    params = {"api_key": API_KEY}
    response = requests.get(url_estaciones, params=params)
    
    if response.status_code == 200:
        data_json = response.json()
        
        if "datos" in data_json:
            data_url = data_json["datos"]
            data_response = requests.get(data_url)

            if data_response.status_code == 200:
                estaciones = data_response.json()
                df = pd.DataFrame(estaciones)

                # Filtrar estaciones de la Comunidad Valenciana
                provincias_cv = ["ALICANTE", "VALENCIA", "CASTELLÓN"]
                df_cv = df[df["provincia"].str.upper().isin(provincias_cv)]

                # Convertir coordenadas
                def convertir_coordenadas(latitud, longitud):
                    def convertir(valor, direccion):
                        grados = int(valor[:2])
                        minutos = int(valor[2:4]) / 60
                        decimal = grados + minutos
                        if direccion in ["S", "W"]:
                            decimal = -decimal
                        return decimal

                    latitud_decimal = convertir(latitud[:-1], latitud[-1])
                    longitud_decimal = convertir(longitud[:-1], longitud[-1])
                    return (latitud_decimal, longitud_decimal)

                df_cv["Coordenadas"] = df_cv.apply(lambda row: convertir_coordenadas(row["latitud"], row["longitud"]), axis=1)

                # Asignar estación más cercana a cada puerto
                estaciones_mas_cercanas = {}
                for puerto, coord_puerto in puertos.items():
                    distancia_minima = float("inf")
                    estacion_mas_cercana = None

                    for _, row in df_cv.iterrows():
                        distancia = geodesic(coord_puerto, row["Coordenadas"]).kilometers
                        if distancia < distancia_minima:
                            distancia_minima = distancia
                            estacion_mas_cercana = row["nombre"]

                    estaciones_mas_cercanas[puerto] = (estacion_mas_cercana, distancia_minima)

                estaciones_disponibles = True
            else:
                st.error("❌ No se pudieron obtener los datos de las estaciones.")
        else:
            st.error("❌ No se encontró la clave 'datos' en la respuesta de AEMET.")
    else:
        st.error(f"❌ Error en la solicitud a AEMET: {response.status_code} - {response.text}")
except Exception as e:
    st.error(f"❌ Error en la obtención de datos meteorológicos: {e}")

# 🔹 Interfaz en Streamlit 🔹
st.title("🌊 Estaciones Meteorológicas y Estado del Mar")

# 📌 Mostrar climatología aunque falle el estado del mar
if estaciones_disponibles:
    puerto_seleccionado = st.selectbox("Selecciona un puerto:", list(puertos.keys()))
    estacion_cercana, distancia = estaciones_mas_cercanas.get(puerto_seleccionado, ("No encontrada", None))

    if estacion_cercana != "No encontrada":
        st.write(f"📍 **Estación más cercana:** {estacion_cercana}")
        st.write(f"📏 **Distancia:** {distancia:.2f} km")

# 🔹 MOSTRAR MAPA 🔹
try:
    st.subheader("🗺️ Ubicación en el Mapa")
    mapa = folium.Map(location=puertos[puerto_seleccionado], zoom_start=10)
    folium.Marker(puertos[puerto_seleccionado], popup=puerto_seleccionado, icon=folium.Icon(color="blue")).add_to(mapa)
    folium_static(mapa)
except Exception as e:
    st.error(f"❌ Error al generar el mapa: {e}")

# 🔹 OBTENER Y MOSTRAR DATOS METEOROLÓGICOS EN TIEMPO REAL 🔹
try:
    st.subheader("🌦️ Datos Meteorológicos en Tiempo Real")

    # Obtener el código de la estación más cercana
    codigo_estacion = df_cv[df_cv["nombre"] == estacion_cercana]["indicativo"].values[0]

    # Verificar si el código de la estación está disponible
    if not codigo_estacion:
        st.warning("⚠️ No se encontró un código de estación meteorológica para este puerto.")
    else:
        url_datos_meteo = f"https://opendata.aemet.es/opendata/api/observacion/convencional/datos/estacion/{codigo_estacion}"
        params = {"api_key": API_KEY}
        response_meteo = requests.get(url_datos_meteo, params=params)

        # Verificar si la solicitud fue exitosa
        if response_meteo.status_code == 200:
            data_json_meteo = response_meteo.json()
            
            if "datos" in data_json_meteo:
                data_url_meteo = data_json_meteo["datos"]
                data_response_meteo = requests.get(data_url_meteo)

                if data_response_meteo.status_code == 200:
                    datos_meteo = data_response_meteo.json()
                    df_meteo = pd.DataFrame(datos_meteo)

                    # Verificar si la tabla de datos meteorológicos tiene contenido
                    if df_meteo.empty:
                        st.warning("⚠️ No hay datos meteorológicos disponibles en este momento.")
                    else:
                        # Definir las columnas a mostrar
                        columnas_disponibles = ["fint", "ta", "hr", "vv", "vmax", "dv", "prec", "tamin", "tamax"]

                        # Filtrar solo las columnas que realmente existen en df_meteo
                        columnas_filtradas = [col for col in columnas_disponibles if col in df_meteo.columns]

                        # Mostrar tabla de datos en Streamlit
                        st.dataframe(df_meteo[columnas_filtradas].rename(columns={
                            "fint": "Fecha/Hora",
                            "ta": "Temperatura (°C)",
                            "hr": "Humedad (%)",
                            "vv": "Velocidad del Viento (km/h)",
                            "vmax": "Ráfaga Máxima de Viento (km/h)",
                            "dv": "Dirección del Viento (°)",
                            "prec": "Precipitación (mm)",
                            "tamin": "Temperatura Mínima (°C)",
                            "tamax": "Temperatura Máxima (°C)"
                        }))
                else:
                    st.warning(f"⚠️ No se pudieron obtener los datos meteorológicos. Código HTTP: {data_response_meteo.status_code}")
            else:
                st.warning("⚠️ AEMET no proporcionó una URL con datos meteorológicos.")
        else:
            st.warning(f"⚠️ Error en la solicitud de datos meteorológicos. Código HTTP: {response_meteo.status_code}")
except Exception as e:
    st.error(f"❌ Error en la obtención de datos meteorológicos: {e}")







# 🔹 OBTENER Y MOSTRAR EL ESTADO DEL MAR 🔹
try:
    st.subheader("🌊 Estado del Mar (AEMET)")
    
    url_base = "https://opendata.aemet.es/opendata/api/prediccion/maritima/costera/costa/46/"
    params = {"api_key": API_KEY}
    response = requests.get(url_base, params=params)

    if response.status_code == 200:
        data_json = response.json()

        if "datos" in data_json:
            data_url = data_json["datos"]
            data_response = requests.get(data_url)

            if data_response.status_code == 200:
                datos_mar_json = data_response.json()

                # Extraer la descripción textual del estado del mar
                estado_mar_texto = datos_mar_json[0].get("situacion", {}).get("texto", "No disponible")

                # Mostrar información en Streamlit
                st.write(f"📅 **Elaborado el:** {datos_mar_json[0]['origen']['elaborado']}")
                st.write(f"📅 **Válido desde:** {datos_mar_json[0]['origen']['inicio']} hasta {datos_mar_json[0]['origen']['fin']}")
                st.write(f"⚠️ **Avisos:** {datos_mar_json[0]['aviso']['texto']}")
                st.write(f"🌊 **Descripción:** {estado_mar_texto}")

            else:
                st.warning("⚠️ No se pudieron obtener los datos reales del estado del mar.")
        else:
            st.warning("⚠️ AEMET no proporcionó una URL con datos del mar.")
    else:
        st.warning(f"⚠️ Error en la solicitud de estado del mar. Código HTTP: {response.status_code}")
except Exception as e:
    st.error(f"❌ Error en la obtención de datos marítimos: {e}")