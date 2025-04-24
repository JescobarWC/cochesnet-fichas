
import streamlit as st
import requests
from bs4 import BeautifulSoup

# ---- Función que busca la URL del coche en coches.net ----
def buscar_url_cochesnet(marca, modelo, acabado):
    query = f"{marca} {modelo} {acabado} site:coches.net/ficha-tecnica"
    res = requests.get("https://www.google.com/search", params={"q": query}, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(res.text, "html.parser")
    for link in soup.find_all("a"):
        href = link.get("href")
        if "coches.net/ficha-tecnica" in href:
            clean_url = href.split("&")[0].replace("/url?q=", "")
            return clean_url
    return None

# ---- Función que scrapea datos técnicos del coche ----
def obtener_ficha_tecnica(url):
    headers = {"User-Agent": "Mozilla/5.0"}
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

# ---- Interfaz Streamlit ----
st.set_page_config(page_title="Ficha Técnica Coches.net", layout="centered")
st.title("Ficha Técnica de Coches")

with st.form("consulta_form"):
    marca = st.text_input("Marca", placeholder="Ej: Seat")
    modelo = st.text_input("Modelo", placeholder="Ej: León")
    acabado = st.text_input("Acabado / versión", placeholder="Ej: FR 1.5 TSI 130cv")
    submitted = st.form_submit_button("Buscar")

if submitted:
    st.info("Buscando en coches.net...")
    url = buscar_url_cochesnet(marca, modelo, acabado)

    if url:
        st.success(f"Ficha técnica encontrada: [Ver en coches.net]({url})")
        ficha = obtener_ficha_tecnica(url)
        if ficha:
            st.subheader("Características técnicas")
            for k, v in ficha.items():
                st.markdown(f"**{k}**: {v}")
        else:
            st.warning("No se pudieron extraer los datos técnicos.")
    else:
        st.error("No se encontró ninguna ficha técnica para ese modelo en coches.net")
