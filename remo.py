import requests
import streamlit as st
import folium
from streamlit_folium import folium_static
import time
from streamlit_javascript import st_javascript
# ---------------------------------------------------------------------------------------------------------
# Detectar el tipo de dispositivo desde el que se está visualizando
# ---------------------------------------------------------------------------------------------------------



# Activar pantalla ancha
st.set_page_config(layout="wide")

# Detectar ancho de pantalla
width = st_javascript("window.innerWidth")
layout = "desktop" if width and int(width) > 800 else "mobile"

# st.write(f"📱 Dispositivo detectado: {layout} (Ancho: {width}px)")
if layout == "desktop":
    col1, col2, col3 = st.columns([1, 3, 1])  # Menú pequeño, contenido más grande
else:
    col1, col2, col3  = st.columns([1, 1, 1])  # En móvil, columnas iguales

# Crear columnas para centrar contenido
# col1, col2, col3 = st.columns([1, 3, 1])  # Columna central más ancha

with col2:  # Todo centrado en la columna central
    # st.markdown("Predicción del Estado del Mar", unsafe_allow_html=True)
    st.markdown("""
        <div style="display: flex; justify-content: center;">
            Estado de la Mar (Viento. Puedes pinchar en el texto viento de la imagen para cambiar el modelo)
        </div>
    """, unsafe_allow_html=True)   
    # Alinear el iframe con CSS
    # st.markdown("""
    #    <div style="display: flex; justify-content: center;">
    #        <iframe src="https://embed.windy.com/embed2.html?lat=38.35&lon=-0.48&zoom=8&level=surface&overlay=wind"
    #                width="1040" height="500" frameborder="0">
    #        </iframe>
    #    </div>
    #""", unsafe_allow_html=True)

    # Detectar ancho de pantalla con un identificador único

    # st.write(f"📱 Dispositivo detectado: {layout} (Ancho: {width}px)")

    # Ajustar tamaño del iframe
    iframe_width = "100%" if layout == "mobile" else "800px"
    iframe_height = "300px" if layout == "mobile" else "500px"

    # Insertar iframe responsivo con CSS
    st.markdown(f"""
        <style>
            .iframe-container {{
                display: flex;
                justify-content: center;
                width: 100%;
            }}
            .responsive-iframe {{
                width: {iframe_width};
                height: {iframe_height};
                max-width: 100%;
                border: none;
            }}
        </style>
        <div class="iframe-container">
            <iframe class="responsive-iframe" 
                    src="https://embed.windy.com/embed2.html?lat=38.35&lon=-0.48&zoom=8&level=surface&overlay=wind">
            </iframe>
        </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------------------------------------
# DICCIONARIO PUERTOS -> CÓDIGO PORTUARIO
# ---------------------------------------------------------------------------------------------------------
# 📌 Diccionario con los códigos reales de los puertos
codigos_puertos_estado = {
    "Puerto de Alicante": "16130",
    "La Albufereta (Alicante)":"36141",
    "San Juan (Alicante)": "36141",
    "Puerto de Altea": "26118",
    "Puerto de Benidorm": "26117",
    "Puerto El Grau de Burriana": "26207",
    "Puerto de Calpe": "26119",
    "Puerto de Castellón": "16240",
    "Puerto de Cullera": "26204",
    "Puerto de Dénia": "26202",
    "Puerto de El Campello": "26115",
    "Puerto de Gandía": "16210",
    "Puerto Guardamar del Segura": "26112",
    "Puerto de Jávea": "26201",
    "Pau Pi (Oliva)": "36261",
    "Puerto de Oropesa": "26210",
    "Puerto de Peñíscola": "26212",
    "Puerto de Pilar de la Horadada": "36110",
    "Puerto de Santa Pola": "26113",
    "Puerto de Sagunto": "16230",
    "Puerto de Torrevieja": "26111",
    "Puerto de Valencia": "16220",
    "Puerto de Villajoyosa": "26116",
    "Puerto de Vinaroz": "16250",
}
# ---------------------------------------------------------------------------------------------------------
#  ESTADO DE LA MAR
# ---------------------------------------------------------------------------------------------------------
# 📌 Guardar el estado del puerto seleccionado en la sesión de Streamlit
if "puerto_actual" not in st.session_state:
    st.session_state.puerto_actual = None

# 📌 Selector de puerto ordenado alfabéticamente
with col1:
    puerto_seleccionado = st.selectbox("Selecciona un puerto:", sorted(codigos_puertos_estado.keys()))

# 📌 Obtener el código del puerto
codigo_puerto = codigos_puertos_estado.get(puerto_seleccionado, None)

# 📌 Si el usuario cambia de puerto, forzar la actualización del iframe
if puerto_seleccionado != st.session_state.puerto_actual:
    st.session_state.puerto_actual = puerto_seleccionado  # Guardamos el nuevo puerto seleccionado
    st.session_state.widget_contador = time.time()  # Nuevo valor único para evitar caché

    # 📌 Forzar una limpieza del iframe antes de recargarlo
    # st.markdown("⚠️ Cargando datos de Puertos del Estado...")
    time.sleep(0.5)  # Esperar 0.5 segundos antes de insertar el nuevo iframe
    st.markdown("")  # Limpiar el widget

# 📌 Generar la URL del widget
if codigo_puerto:
# 📌 Contenedor dinámico para el widget
    contenedor_widget = st.empty()

# 📌 Mensaje de carga mientras cambia el widget
#    with contenedor_widget:
    with col2:
        # st.warning("⚠️ Cargando datos de Puertos del Estado...")

# 📌 Generar la URL del widget con un "cache buster" para forzar recarga
        cache_buster = int(time.time())  # Genera un número aleatorio basado en el tiempo
        url_widget = f"https://portus.puertos.es/#/locationsWidget?code={codigo_puerto}&theme=dark&locale=es&cache_buster={cache_buster}"

# 📌 Vaciar el contenedor antes de insertar el nuevo `iframe`
        contenedor_widget.empty()
        time.sleep(1)  # Pequeña pausa para asegurar que Streamlit no conserve caché

# 📌 Mostrar el nuevo widget
     #   contenedor_widget.markdown(
     #           f"""
     #           <div style="display: flex; justify-content: center;">
     #               <iframe width="1040" height="570" src="{url_widget}" frameborder="0"></iframe>
     #           </div>
     #           <br>
     #           <p style="text-align: center; font-size: 14px;">
     #               ℹ️ <b>Para ampliar información sobre este puerto, visita 
     #           <a href="https://portus.puertos.es" target="_blank">Portus - Puertos del Estado</a></b> 🌍
     #           </p>
     #           """,
     #       unsafe_allow_html=True
     #   )
# -.-.-.
    # Ajustar tamaño del iframe
        iframe_width = "100%" if layout == "mobile" else "900px"
        iframe_height = "400px" if layout == "mobile" else "500px"

     


    # Insertar iframe responsivo con CSS
        contenedor_widget.markdown(f"""
                <style>
                    .iframe-container {{
                        display: flex;
                        justify-content: center;
                        width: 100%;
                    }}
                    .responsive-iframe {{
                        width: {iframe_width};
                        height: {iframe_height};
                        max-width: 100%;
                        border: none;
                    }}
                </style>
                <div class="iframe-container">
                    <iframe class="responsive-iframe" 
                        src="{url_widget}" frameborder="0">
                    </iframe>
                </div>
                <br>
                <p style="text-align: center; font-size: 14px;">
                    ℹ️ <b>Para ampliar información sobre este puerto, visita 
                <a href="https://portus.puertos.es" target="_blank">Portus - Puertos del Estado</a></b> 🌍
                </p>
            """, unsafe_allow_html=True)

   


#-.-.-.-.
else:
    st.warning("⚠️ No se encontró el código del puerto seleccionado.")
# ---------------------------------------------------------------------------------------------------------
#  A  E  M  E  T
# ---------------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------------
# API Key de AEMET
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJkYW5pZWxtb3lhZnVzdGVyQGdtYWlsLmNvbSIsImp0aSI6ImE5YzRlYzA2LTQ5ZmMtNGIyZi04OGU4LWRjNTQ1MDA1MThmYiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNzQwNjY4MjQ4LCJ1c2VySWQiOiJhOWM0ZWMwNi00OWZjLTRiMmYtODhlOC1kYzU0NTAwNTE4ZmIiLCJyb2xlIjoiIn0.FPSuXda0P6PeRFZ80LHCW-O6cMdMR8RLTFl_pBKQ6q4"
# ---------------------------------------------------------------------------------------------------------

# ✅ Diccionario de códigos de municipios
codigos_municipios_puertos = {
    "Puerto de Alicante": "03014",
    "Puerto de Castellón": "12040",
    "Puerto de Gandía": "46131",
    "Puerto de Valencia": "06139",
    "Puerto de Dénia": "03063",
    "La Albufereta (Alicante)":"03014",
    "San Juan (Alicante)": "03119",
    "Puerto de Altea": "03018",
    "Puerto de Benidorm": "03031",
    "Puerto El Grau de Burriana": "12032",
    "Puerto de Calpe": "03047",
    "Puerto de Castellón": "12040",
    "Puerto de Cullera": "46105",
    "Puerto de Dénia": "03063",
    "Puerto de El Campello": "03050",
    "Puerto de Gandía": "46211",
    "Puerto Guardamar del Segura": "03076",
    "Puerto de Jávea": "03082",
    "Pau Pi (Oliva)": "46181",
    "Puerto de Oropesa": "12085",
    "Puerto de Peñíscola": "12089",
    "Puerto de Pilar de la Horadada": "03902",
    "Puerto de Santa Pola": "03121",
    "Puerto de Sagunto": "46220",
    "Puerto de Torrevieja": "03133",
    "Puerto de Valencia": "46250",
    "Puerto de Villajoyosa": "03139",
    "Puerto de Vinaroz": "12138",

    
}

# ✅ Función para obtener la predicción de AEMET
def obtener_prediccion(codigo_municipio):
    url_prediccion = f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/{codigo_municipio}/"
    params = {"api_key": API_KEY}

    try:
        response = requests.get(url_prediccion, params=params)
        if response.status_code == 200:
            data_json = response.json()
            if "datos" in data_json:
                data_url = data_json["datos"]
                data_response = requests.get(data_url)
                if data_response.status_code == 200:
                    return data_response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error en la solicitud a AEMET: {e}")
    
    return None

# ✅ Streamlit: Selector de Puerto
# st.title("🌦️ Predicción Meteorológica")
# puerto_seleccionado = st.selectbox("Selecciona un puerto:", sorted(codigos_municipios_puertos.keys()))

if puerto_seleccionado:
    codigo_municipio = codigos_municipios_puertos[puerto_seleccionado]

    # ✅ Predicción Meteorológica de AEMET
    if codigo_municipio:
        datos_prediccion = obtener_prediccion(codigo_municipio)

        if datos_prediccion and isinstance(datos_prediccion, list):
            try:
                prediccion_hoy = datos_prediccion[0]["prediccion"]["dia"][0]
                prediccion_manana = datos_prediccion[0]["prediccion"]["dia"][1]
                
                fecha_hoy = prediccion_hoy["fecha"][:10]
                fecha_manana = prediccion_manana["fecha"][:10]

                estado_cielo_hoy = next((e["descripcion"] for e in prediccion_hoy["estadoCielo"] if e["periodo"] == "12-24"), "No disponible")
                estado_cielo_manana = next((e["descripcion"] for e in prediccion_manana["estadoCielo"] if e["periodo"] == "12-24"), "No disponible")

                temp_max_hoy, temp_min_hoy = prediccion_hoy["temperatura"]["maxima"], prediccion_hoy["temperatura"]["minima"]
                temp_max_manana, temp_min_manana = prediccion_manana["temperatura"]["maxima"], prediccion_manana["temperatura"]["minima"]
                with col2:
                # ✅ Mostrar solo la predicción en texto

                    # st.markdown(f"<h3 style='text-align: center;'>TIPO: {layout}</h3>", unsafe_allow_html=True) #### dani ###


                    st.markdown(f"<h3 style='text-align: center;'>Predicción para {puerto_seleccionado}</h3>", unsafe_allow_html=True)
                    # st.write(f"Predicción para {puerto_seleccionado}")
                    # st.subheader(f"📡 Predicción para {puerto_seleccionado}")
                    st.markdown(f"<p style='font-size: 18px; text-align: center;'>Predicción para HOY    ({fecha_hoy}): {estado_cielo_hoy}, Temp.Máx.: {temp_max_hoy}°C, Temp.Mín.: {temp_min_hoy}°C</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 18px; text-align: center;'>Predicción para MAÑANA ({fecha_manana}): {estado_cielo_manana}, Temp.Máx.: {temp_max_manana}°C, Temp.Mín.: {temp_min_manana}°C</p>", unsafe_allow_html=True)
                   
                    # st.write(f"📅 **Hoy ({fecha_hoy}):** {estado_cielo_hoy}, 🌡 Máx: {temp_max_hoy}°C, Mín: {temp_min_hoy}°C")
                    # st.write(f"📅 **Mañana ({fecha_manana}):** {estado_cielo_manana}, 🌡 Máx: {temp_max_manana}°C, Mín: {temp_min_manana}°C")

            except KeyError:
                st.warning("⚠️ AEMET no devolvió los datos esperados.")
        else:
            st.warning(f"❌ No se pudo obtener la predicción meteorológica para {puerto_seleccionado}.")