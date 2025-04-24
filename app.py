
import streamlit as st
import requests
from bs4 import BeautifulSoup

# ---- Función que scrapea datos técnicos del coche ----
def obtener_ficha_tecnica(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        caracteristicas = {}
        for fila in soup.select(".fichaTecnica-item"):
            clave_tag = fila.select_one(".fichaTecnica-item-title")
            valor_tag = fila.select_one(".fichaTecnica-item-value")
            if clave_tag and valor_tag:
                clave = clave_tag.text.strip()
                valor = valor_tag.text.strip()
                caracteristicas[clave] = valor

        return caracteristicas
    except Exception as e:
        st.error(f"Error al obtener datos: {e}")
        return None

# ---- Interfaz Streamlit ----
st.set_page_config(page_title="Ficha Técnica Coches.net", layout="centered")
st.title("Ficha Técnica de Coches")

with st.form("consulta_form"):
    url = st.text_input("Pega aquí el enlace de la ficha técnica de coches.net",
                        placeholder="Ej: https://www.coches.net/ficha-tecnica/ford/kuga/2023/...")
    submitted = st.form_submit_button("Obtener datos")

if submitted:
    if url.startswith("http"):
        st.success(f"Analizando: [Ver ficha en coches.net]({url})")
        ficha = obtener_ficha_tecnica(url)
        if ficha:
            st.subheader("Características técnicas")
            for k, v in ficha.items():
                st.markdown(f"**{k}**: {v}")
        else:
            st.warning("No se encontraron características o hubo un error.")
    else:
        st.error("Por favor, introduce una URL válida que empiece por https://")
