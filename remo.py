import streamlit as st
import time

# 📌 Diccionario con los códigos reales de los puertos
codigos_puertos_estado = {
    "Puerto de Alicante": "16130",
    "La Albufereta (Alicante)":"36141",
    "San Juan (Alicante)": "36141",
    "Puerto de Altea": "26118",
    "Puerto de Benidorm": "26117",
    "El Grau de Burriana": "26207",
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

# 📌 Guardar el estado del puerto seleccionado en la sesión de Streamlit
if "puerto_actual" not in st.session_state:
    st.session_state.puerto_actual = None

# 📌 Selector de puerto ordenado alfabéticamente
# puerto_seleccionado = st.selectbox("Selecciona un puerto:", sorted(codigos_puertos_estado.keys()))
puerto_seleccionado = st.selectbox("Selecciona un puerto:")
# 📌 Obtener el código del puerto
codigo_puerto = codigos_puertos_estado.get(puerto_seleccionado, None)

# 📌 Si el usuario cambia de puerto, forzar la actualización del iframe
if puerto_seleccionado != st.session_state.puerto_actual:
    st.session_state.puerto_actual = puerto_seleccionado  # Guardamos el nuevo puerto seleccionado
    st.session_state.widget_contador = time.time()  # Nuevo valor único para evitar caché

    # 📌 Forzar una limpieza del iframe antes de recargarlo
    st.markdown("⚠️ Cargando datos de Puertos del Estado...")
    time.sleep(0.5)  # Esperar 0.5 segundos antes de insertar el nuevo iframe
    st.markdown("")  # Limpiar el widget

# 📌 Generar la URL del widget
if codigo_puerto:
# 📌 Contenedor dinámico para el widget
    contenedor_widget = st.empty()

# 📌 Mensaje de carga mientras cambia el widget
    with contenedor_widget:
        st.warning("⚠️ Cargando datos de Puertos del Estado...")

# 📌 Generar la URL del widget con un "cache buster" para forzar recarga
        cache_buster = int(time.time())  # Genera un número aleatorio basado en el tiempo
        url_widget = f"https://portus.puertos.es/#/locationsWidget?code={codigo_puerto}&theme=dark&locale=es&cache_buster={cache_buster}"

# 📌 Vaciar el contenedor antes de insertar el nuevo `iframe`
        contenedor_widget.empty()
        time.sleep(1)  # Pequeña pausa para asegurar que Streamlit no conserve caché

# 📌 Mostrar el nuevo widget
        contenedor_widget.markdown(
            f'<iframe width="1040" height="570" src="{url_widget}" frameborder="0"></iframe>',
            unsafe_allow_html=True
        )




    # url_widget = f"https://portus.puertos.es/#/locationsWidget?code={codigo_puerto}&theme=dark&locale=es&cache_buster={st.session_state.widget_contador}"
    # 📌 Mostrar el widget con los datos
    # st.markdown(f"### 🌊 **Previsiones y estado actual del mar en el {puerto_seleccionado}.** Todas las horas son GMT.")
    # st.markdown(
    #    f'<iframe src="{url_widget}" width="1040" height="570" frameborder="0"></iframe>',
    #    unsafe_allow_html=True
    #)
else:
    st.warning("⚠️ No se encontró el código del puerto seleccionado.")