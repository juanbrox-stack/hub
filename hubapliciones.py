import streamlit as st
import base64
import pandas as pd
import os

# Configuración de página
st.set_page_config(page_title="Hub de Aplicaciones Turaco", layout="wide", page_icon="🚀")

def get_svg_base64(svg_path):
    """Obtiene el base64 de un SVG para insertarlo en el HTML."""
    try:
        with open(svg_path, "r") as f:
            svg = f.read()
            return base64.b64encode(svg.encode('utf-8')).decode('utf-8')
    except:
        return None

# --- LISTA COMPLETA DE APPS (23 aplicaciones) ---
apps = [
    {"nombre": "Marketplaces", "url": "https://multitienda-bi-group.streamlit.app", "icon": "marketplaces.svg", "desc": "BI de pedidos, análisis por marketplaces y año.", "color": "#FAF9F5", "cat": "BI", "pdf": "Marketplaces.pdf"},
    {"nombre": "Calculadora ROI Automatización", "url": "https://calculadoraretornoinversion.streamlit.app/", "icon": "marketplaces.svg", "desc": "Calcula el ahorro y rentabilidad de proyectos de automatización.", "color": "#FAF9F5", "cat": "Utilidad", "pdf": "Calculadora_ROI_Automatizacion.pdf"},
    {"nombre": "Actualizador Tarifas", "url": "https://actualizardortarifas.streamlit.app", "icon": "actualizardortarifas.svg", "desc": "Gestión y actualización de tarifas, genera el fichero completo.", "color": "#FAF9F5", "cat": "Tarifas", "pdf": "Actualizador Tarifas.pdf"},
    {"nombre": "Extractor de URLs para PrestaShop", "url": "https://concatenarurl.streamlit.app/", "icon": "marketplaces.svg", "desc": "Generador de URLs absolutas para imágenes de productos.", "color": "#FAF9F5", "cat": "Catálogo", "pdf": "Extractor de URLs para PrestaShop.pdf"},
    {"nombre": "Cecotec Downloader", "url": "https://cecotec-downloader.streamlit.app", "icon": "cecotec-downloader.svg", "desc": "Descarga de catálogos y datos de la web de Cecotec.", "color": "#FAF9F5", "cat": "Scraping", "pdf": "Cecotec Downloader.pdf"},
    {"nombre": "Features PS", "url": "https://featuresps.streamlit.app", "icon": "featuresps.svg", "desc": "Creación de fichero de características técnicas PrestaShop.", "color": "#FAF9F5", "cat": "Catálogo", "pdf": "Features PS.pdf"},
    {"nombre": "Características 2026", "url": "https://caracteristicaspsturaco2026.streamlit.app/", "icon": "featuresps.svg", "desc": "Gestión avanzada de características PrestaShop 2026.", "color": "#FAF9F5", "cat": "Catálogo", "pdf": "Características 2026.pdf"},
    {"nombre": "Errors", "url": "https://errors.streamlit.app/", "icon": "marketplaces.svg", "desc": "Analizar errores de publicación Mirakl / Marketplaces.", "color": "#FAF9F5", "cat": "Errores", "pdf": "Errors.pdf"},
    {"nombre": "Errores BeezUP", "url": "https://erroresbeezup.streamlit.app/", "icon": "marketplaces.svg", "desc": "Gestor de errores de publicación específicos de BeezUP.", "color": "#FAF9F5", "cat": "Errores", "pdf": "Errores BeezUP.pdf"},
    {"nombre": "Variaciones Cdiscount", "url": "https://variacionescdiscount.streamlit.app/", "icon": "marketplaces.svg", "desc": "Generador de variaciones específicas para Cdiscount.", "color": "#FAF9F5", "cat": "Catálogo", "pdf": "Variaciones Cdiscount.pdf"},
    {"nombre": "Map Categories", "url": "https://mapcategories.streamlit.app", "icon": "mapcategories.svg", "desc": "Mapeo lógico de categorías Amazon vs PrestaShop.", "color": "#FAF9F5", "cat": "Logística", "pdf": "Map Categories.pdf"},
    {"nombre": "PS Bridge", "url": "https://ps-bridge.streamlit.app", "icon": "ps-bridge.svg", "desc": "Fichero de subida de novedades a PrestaShop.", "color": "#FAF9F5", "cat": "Catálogo", "pdf": "PS Bridge.pdf"},
    {"nombre": "Stock Amazon", "url": "https://stockamazon.streamlit.app", "icon": "stockamazon.svg", "desc": "Gestión de stock (convertir antes si no es .xlsx).", "color": "#FAF9F5", "cat": "Stock", "has_step_prior": True, "prior_url": "https://convertirexcels.streamlit.app/", "pdf": "Stock Amazon.pdf"},
    {"nombre": "Seguimientos Amazon", "url": "https://seguimientosamazon.streamlit.app/", "icon": "stockamazon.svg", "desc": "Seguimiento y control de pedidos en Amazon.", "color": "#FAF9F5", "cat": "Logística", "pdf": "Seguimientos Amazon.pdf"},
    {"nombre": "Amazon Facturas", "url": "https://transformarexcelamazonfacturas.streamlit.app/", "icon": "stockamazon.svg", "desc": "Transformación de ficheros para facturación Amazon.", "color": "#FAF9F5", "cat": "Facturación", "pdf": "Amazon Facturas.pdf"},
    {"nombre": "Dividir Excel", "url": "https://dividirexcel.streamlit.app/", "icon": "marketplaces.svg", "desc": "Separa archivos Excel en múltiples pestañas o ficheros.", "color": "#FAF9F5", "cat": "Utilidad", "pdf": "Dividir Excel.pdf"},
    {"nombre": "Revisar URL Fotos", "url": "https://revisarurlimagenes.streamlit.app/", "icon": "marketplaces.svg", "desc": "Validación masiva de URLs de imágenes (Evita 404).", "color": "#FAF9F5", "cat": "Calidad", "pdf": "Revisar URL Fotos.pdf"},
    {"nombre": "Actualiza URLs", "url": "https://actualizaurlsimagenes.streamlit.app/", "icon": "marketplaces.svg", "desc": "Edición masiva de rutas de imágenes en ficheros.", "color": "#FAF9F5", "cat": "Catálogo", "pdf": "Actualiza URLs.pdf"},
    {"nombre": "Comparar PS vs Amazon", "url": "https://compararpsvsamazon.streamlit.app/", "icon": "marketplaces.svg", "desc": "Auditoría de catálogo PrestaShop vs Amazon.", "color": "#FAF9F5", "cat": "Auditoría", "pdf": "Comparar PS vs Amazon.pdf"},
    {"nombre": "Reviews Tracker", "url": "https://reviewstracker.streamlit.app", "icon": "marketplaces.svg", "desc": "Seguimiento y análisis de reseñas de clientes.", "color": "#FAF9F5", "cat": "Marketing", "pdf": "Reviews Tracker.pdf"},
    {"nombre": "Unidad Nueva", "url": "https://unidadnueva.streamlit.app", "icon": "unidadnueva.svg", "desc": "Subida a Cecopartners de pedidos automatizada.", "color": "#FAF9F5", "cat": "Catálogo", "pdf": "Unidad Nueva.pdf"},
    {"nombre": "Tipo Dispositivo", "url": "https://tipodispositivo.streamlit.app/", "icon": "marketplaces.svg", "desc": "Identificación del tipo de dispositivo de acceso.", "color": "#FAF9F5", "cat": "Utilidad", "pdf": "Tipo Dispositivo.pdf"},
    {"nombre": "Recortador Cadenas", "url": "https://recortadorcadenastexto.streamlit.app/", "icon": "marketplaces.svg", "desc": "Limpieza y recorte de longitud de textos.", "color": "#FAF9F5", "cat": "Utilidad", "pdf": "Recortador Cadenas.pdf"}
]

# Estilos CSS
st.markdown("""
    <style>
    /* Fondo Negro para el panel */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }

    /* Títulos y textos descriptivos de la tarjeta */
    .card-title { color: #111111 !important; margin: 0; font-size: 1.2rem; font-weight: 800; line-height: 1.1; }
    .card-desc { color: #333333 !important; font-size: 0.85rem; margin-top: 5px; line-height: 1.2; font-weight: 500; }
    
    .app-card {
        padding: 12px 15px; border-radius: 12px; border: 1px solid #333;
        text-align: center; min-height: 145px; display: flex;
        flex-direction: column; justify-content: center; align-items: center; margin-bottom: 10px;
        background-color: #FAF9F5;
    }

    /* Forzar centrado de los contenedores de botones */
    [data-testid="stVerticalBlock"] > div:has(div.stButton), 
    [data-testid="stVerticalBlock"] > div:has(div.stDownloadButton) {
        display: flex;
        justify-content: center;
        width: 100%;
    }

    /* BOTONES: Color #3EB1C8 y Texto Gris Claro #E0E0E0 */
    div.stButton > button, div.stDownloadButton > button {
        background-color: #3EB1C8 !important; 
        color: #E0E0E0 !important;
        border-radius: 8px !important;
        font-weight: bold !important; 
        font-size: 0.8rem !important; 
        height: 2.6em !important; 
        width: 160px !important;
        margin: 5px auto !important; 
        border: none !important;
        display: flex;
        justify-content: center;
        align-items: center;
        transition: all 0.3s ease;
    }
    
    /* HOVER: Texto en Blanco puro al pasar el ratón */
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background-color: #359fb4 !important;
        color: #ffffff !important;
        border: none !important;
    }

    /* Caja de introducción */
    .intro-box { 
        background-color: #1a1a1a; 
        padding: 12px; 
        border-radius: 10px; 
        border-left: 5px solid #3EB1C8; 
        margin-bottom: 15px; 
    }

    /* Ajustes para el índice rápido */
    .stExpander {
        background-color: #111111 !important;
        border: 1px solid #333 !important;
    }
    a { color: #3EB1C8 !important; text-decoration: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Panel Central de Aplicaciones Turaco")

st.markdown("""
<div class="intro-box">
    <p style="margin:0; font-size:0.9rem; color:white;">Hub de herramientas para la gestión de Marketplaces. Usa el <b>Índice</b> para navegación rápida o descarga los <b>Manuales</b> de estructura.</p>
</div>
""", unsafe_allow_html=True)

search_query = st.text_input("🔍 Buscar aplicación...", "").lower()

if not search_query:
    with st.expander("📊 Índice rápido de acceso directo", expanded=False):
        df_index = pd.DataFrame([{"Aplicación": f'<a href="{a["url"]}" target="_blank">{a["nombre"]}</a>', "Categoría": a['cat'], "Función": a['desc']} for a in apps])
        st.write(df_index.to_html(escape=False, index=False), unsafe_allow_html=True)

apps_filtradas = [app for app in apps if search_query in app["nombre"].lower() or search_query in app["desc"].lower() or search_query in app["cat"].lower()]

st.markdown("---")

if apps_filtradas:
    cols = st.columns(4)
    for i, app in enumerate(apps_filtradas):
        with cols[i % 4]:
            b64_icon = get_svg_base64(f"iconos/{app['icon']}")
            icon_html = f'<img src="data:image/svg+xml;base64,{b64_icon}" width="35" style="margin-bottom:5px;"/>' if b64_icon else "📦"
            
            st.markdown(f"""
                <div class="app-card">
                    <div>
                        {icon_html}
                        <div class="card-title">{app['nombre']}</div>
                        <div class="card-desc">{app['desc']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # BOTÓN MANUAL
            pdf_path = f"Estructura PDF/{app['pdf']}"
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="📂 Manual",
                        data=f,
                        file_name=app['pdf'],
                        mime="application/pdf",
                        key=f"dl_{i}"
                    )
            else:
                st.button("📄 Sin Manual", disabled=True, key=f"none_{i}")

            # BOTONES DE ACCESO
            if app.get("has_step_prior"):
                c1, c2 = st.columns(2)
                with c1: st.link_button("❶ Conv", app['prior_url'], use_container_width=True)
                with c2: st.link_button("❷ Stock", app['url'], use_container_width=True)
            else:
                st.link_button("Abrir Aplicación", app['url'], use_container_width=True)
else:
    st.warning("No se encontraron coincidencias.")