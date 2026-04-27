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

# --- LISTA COMPLETA DE APPS (21 aplicaciones) ---
apps = [
    {"nombre": "Marketplaces", "url": "https://multitienda-bi-group.streamlit.app", "icon": "marketplaces.svg", "desc": "BI de pedidos, análisis por marketplaces y año.", "color": "#e3f2fd", "cat": "BI", "pdf": "Marketplaces.pdf"},
    {"nombre": "Actualizador Tarifas", "url": "https://actualizardortarifas.streamlit.app", "icon": "actualizardortarifas.svg", "desc": "Gestión y actualización de tarifas, genera el fichero completo.", "color": "#fff3e0", "cat": "Tarifas", "pdf": "Actualizador Tarifas.pdf"},
    {"nombre": "Cecotec Downloader", "url": "https://cecotec-downloader.streamlit.app", "icon": "cecotec-downloader.svg", "desc": "Descarga de catálogos y datos de la web de Cecotec.", "color": "#f3e5f5", "cat": "Scraping", "pdf": "Cecotec Downloader.pdf"},
    {"nombre": "Features PS", "url": "https://featuresps.streamlit.app", "icon": "featuresps.svg", "desc": "Creación de fichero de características técnicas PrestaShop.", "color": "#efebe9", "cat": "Catálogo", "pdf": "Features PS.pdf"},
    {"nombre": "Características 2026", "url": "https://caracteristicaspsturaco2026.streamlit.app/", "icon": "featuresps.svg", "desc": "Gestión avanzada de características PrestaShop 2026.", "color": "#e1f5fe", "cat": "Catálogo", "pdf": "Características 2026.pdf"},
    {"nombre": "Errors", "url": "https://errors.streamlit.app/", "icon": "marketplaces.svg", "desc": "Analizar errores de publicación Mirakl / Marketplaces.", "color": "#ffebee", "cat": "Errores", "pdf": "Errors.pdf"},
    {"nombre": "Errores BeezUP", "url": "https://erroresbeezup.streamlit.app/", "icon": "marketplaces.svg", "desc": "Gestor de errores de publicación específicos de BeezUP.", "color": "#fff3e0", "cat": "Errores", "pdf": "Errores BeezUP.pdf"},
    {"nombre": "Variaciones Cdiscount", "url": "https://variacionescdiscount.streamlit.app/", "icon": "marketplaces.svg", "desc": "Generador de variaciones específicas para Cdiscount.", "color": "#fce4ec", "cat": "Catálogo", "pdf": "Variaciones Cdiscount.pdf"},
    {"nombre": "Map Categories", "url": "https://mapcategories.streamlit.app", "icon": "mapcategories.svg", "desc": "Mapeo lógico de categorías Amazon vs PrestaShop.", "color": "#e0f2f1", "cat": "Logística", "pdf": "Map Categories.pdf"},
    {"nombre": "PS Bridge", "url": "https://ps-bridge.streamlit.app", "icon": "ps-bridge.svg", "desc": "Fichero de subida de novedades a PrestaShop.", "color": "#e8eaf6", "cat": "Catálogo", "pdf": "PS Bridge.pdf"},
    {"nombre": "Stock Amazon", "url": "https://stockamazon.streamlit.app", "icon": "stockamazon.svg", "desc": "Gestión de stock (convertir antes si no es .xlsx).", "color": "#fffde7", "cat": "Stock", "has_step_prior": True, "prior_url": "https://convertirexcels.streamlit.app/", "pdf": "Stock Amazon.pdf"},
    {"nombre": "Seguimientos Amazon", "url": "https://seguimientosamazon.streamlit.app/", "icon": "stockamazon.svg", "desc": "Seguimiento y control de pedidos en Amazon.", "color": "#eceff1", "cat": "Logística", "pdf": "Seguimientos Amazon.pdf"},
    {"nombre": "Amazon Facturas", "url": "https://transformarexcelamazonfacturas.streamlit.app/", "icon": "stockamazon.svg", "desc": "Transformación de ficheros para facturación Amazon.", "color": "#f3e5f5", "cat": "Facturación", "pdf": "Amazon Facturas.pdf"},
    {"nombre": "Dividir Excel", "url": "https://dividirexcel.streamlit.app/", "icon": "marketplaces.svg", "desc": "Separa archivos Excel en múltiples pestañas o ficheros.", "color": "#ede7f6", "cat": "Utilidad", "pdf": "Dividir Excel.pdf"},
    {"nombre": "Revisar URL Fotos", "url": "https://revisarurlimagenes.streamlit.app/", "icon": "marketplaces.svg", "desc": "Validación masiva de URLs de imágenes (Evita 404).", "color": "#fff8e1", "cat": "Calidad", "pdf": "Revisar URL Fotos.pdf"},
    {"nombre": "Actualiza URLs", "url": "https://actualizaurlsimagenes.streamlit.app/", "icon": "marketplaces.svg", "desc": "Edición masiva de rutas de imágenes en ficheros.", "color": "#e0f7fa", "cat": "Catálogo", "pdf": "Actualiza URLs.pdf"},
    {"nombre": "Comparar PS vs Amazon", "url": "https://compararpsvsamazon.streamlit.app/", "icon": "marketplaces.svg", "desc": "Auditoría de catálogo PrestaShop vs Amazon.", "color": "#e8f5e9", "cat": "Auditoría", "pdf": "Comparar PS vs Amazon.pdf"},
    {"nombre": "Reviews Tracker", "url": "https://reviewstracker.streamlit.app", "icon": "marketplaces.svg", "desc": "Seguimiento y análisis de reseñas de clientes.", "color": "#f0f4c3", "cat": "Marketing", "pdf": "Reviews Tracker.pdf"},
    {"nombre": "Unidad Nueva", "url": "https://unidadnueva.streamlit.app", "icon": "unidadnueva.svg", "desc": "Subida a Cecopartners de pedidos automatizada.", "color": "#fbe9e7", "cat": "Catálogo", "pdf": "Unidad Nueva.pdf"},
    {"nombre": "Tipo Dispositivo", "url": "https://tipodispositivo.streamlit.app/", "icon": "marketplaces.svg", "desc": "Identificación del tipo de dispositivo de acceso.", "color": "#f5f5f5", "cat": "Utilidad", "pdf": "Tipo Dispositivo.pdf"},
    {"nombre": "Recortador Cadenas", "url": "https://recortadorcadenastexto.streamlit.app/", "icon": "marketplaces.svg", "desc": "Limpieza y recorte de longitud de textos.", "color": "#eceff1", "cat": "Utilidad", "pdf": "Recortador Cadenas.pdf"}
]

# Estilos CSS
st.markdown("""
    <style>
    .card-title { color: #111; margin: 0; font-size: 1.2rem; font-weight: 800; line-height: 1.1; }
    .card-desc { color: #333; font-size: 0.85rem; margin-top: 5px; line-height: 1.2; font-weight: 500; }
    .app-card {
        padding: 12px 15px; border-radius: 12px; border: 1px solid #e0e0e0;
        text-align: center; min-height: 145px; display: flex;
        flex-direction: column; justify-content: center; align-items: center; margin-bottom: 5px;
    }
    div.stButton > button, div.stDownloadButton > button {
        background-color: #007bff !important; color: white !important; border-radius: 8px !important;
        font-weight: bold !important; font-size: 0.8rem !important; height: 2.5em !important; width: 100% !important;
        margin-top: 2px !important; border: none !important;
    }
    .stDownloadButton > button {
        background-color: #ffffff !important; color: #007bff !important; border: 1px solid #007bff !important;
    }
    .intro-box { background-color: #f8f9fa; padding: 12px; border-radius: 10px; border-left: 5px solid #007bff; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Panel Central de Aplicaciones Turaco")

# SECCIÓN: INTRODUCCIÓN
st.markdown("""
<div class="intro-box">
    <p style="margin:0; font-size:0.9rem;">Hub de herramientas para la gestión de Marketplaces. Usa el <b>Índice</b> para navegación rápida o descarga los <b>Manuales</b> de estructura.</p>
</div>
""", unsafe_allow_html=True)

# BUSCADOR
search_query = st.text_input("🔍 Buscar aplicación...", "").lower()

# ÍNDICE RÁPIDO (Visible cuando no hay búsqueda activa)
if not search_query:
    with st.expander("📊 Índice rápido de acceso directo", expanded=False):
        df_index = pd.DataFrame([{"Aplicación": f'<a href="{a["url"]}" target="_blank">{a["nombre"]}</a>', "Categoría": a['cat'], "Función": a['desc']} for a in apps])
        st.write(df_index.to_html(escape=False, index=False), unsafe_allow_html=True)

apps_filtradas = [app for app in apps if search_query in app["nombre"].lower() or search_query in app["desc"].lower() or search_query in app["cat"].lower()]

st.markdown("---")

# GRID DE TARJETAS
if apps_filtradas:
    cols = st.columns(4)
    for i, app in enumerate(apps_filtradas):
        with cols[i % 4]:
            b64_icon = get_svg_base64(f"iconos/{app['icon']}")
            icon_html = f'<img src="data:image/svg+xml;base64,{b64_icon}" width="35" style="margin-bottom:5px;"/>' if b64_icon else "📦"
            
            st.markdown(f"""
                <div class="app-card" style="background-color: {app['color']};">
                    <div>
                        {icon_html}
                        <div class="card-title">{app['nombre']}</div>
                        <div class="card-desc">{app['desc']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # BOTÓN DESCARGA MANUAL
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