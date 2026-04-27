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
    except FileNotFoundError:
        return None

def get_pdf_download_link(pdf_path, label):
    """Genera un botón de descarga para un archivo PDF local."""
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        return f'<a href="data:application/pdf;base64,{base64_pdf}" download="{os.path.basename(pdf_path)}" style="text-decoration: none; color: #007bff; font-weight: bold; font-size: 0.85rem;">📂 Estructura PDF</a>'
    return '<span style="color: #ccc; font-size: 0.8rem;">📄 Sin PDF</span>'

# LISTA ACTUALIZADA DE APPS (21 aplicaciones)
apps = [
    {"nombre": "Marketplaces", "url": "https://multitienda-bi-group.streamlit.app", "icon": "marketplaces.svg", "desc": "Business Intelligence de pedidos, análisis por marketplaces y año.", "color": "#e3f2fd", "cat": "BI & Ventas", "pdf": "marketplaces.pdf"},
    {"nombre": "Actualizador Tarifas", "url": "https://actualizardortarifas.streamlit.app", "icon": "actualizardortarifas.svg", "desc": "Gestión y actualización de tarifas, genera el fichero con la tarifa completa.", "color": "#fff3e0", "cat": "Tarifas", "pdf": "tarifas.pdf"},
    {"nombre": "Cecotec Downloader", "url": "https://cecotec-downloader.streamlit.app", "icon": "cecotec-downloader.svg", "desc": "Herramienta de descarga de catálogos y datos de las web de Cecotec.", "color": "#f3e5f5", "cat": "Scraping", "pdf": "downloader.pdf"},
    {"nombre": "Features PS", "url": "https://featuresps.streamlit.app", "icon": "featuresps.svg", "desc": "Creación del fichero de subida de características técnicas en PrestaShop.", "color": "#efebe9", "cat": "Catálogo", "pdf": "features.pdf"},
    {"nombre": "Características 2026", "url": "https://caracteristicaspsturaco2026.streamlit.app/", "icon": "featuresps.svg", "desc": "Nueva utilidad 2026 para la gestión avanzada de características en PrestaShop.", "color": "#e1f5fe", "cat": "Catálogo", "pdf": "features2026.pdf"},
    {"nombre": "Errors", "url": "https://errors.streamlit.app/", "icon": "marketplaces.svg", "desc": "Analizar errores de publicación en marketplaces. Subir fichero de Mirakl.", "color": "#ffebee", "cat": "Errores", "pdf": "errores_mirakl.pdf"},
    {"nombre": "Errores BeezUP", "url": "https://erroresbeezup.streamlit.app/", "icon": "marketplaces.svg", "desc": "Analizador y gestor de errores de publicación específicos de BeezUP.", "color": "#fff3e0", "cat": "Errores", "pdf": "beezup.pdf"},
    {"nombre": "Variaciones Cdiscount", "url": "https://variacionescdiscount.streamlit.app/", "icon": "marketplaces.svg", "desc": "Generador de variaciones y combinaciones específicas para Cdiscount.", "color": "#fce4ec", "cat": "Catálogo", "pdf": "cdiscount.pdf"},
    {"nombre": "Map Categories", "url": "https://mapcategories.streamlit.app", "icon": "mapcategories.svg", "desc": "Mapeo lógico y organización de categorías Amazon vs PS.", "color": "#e0f2f1", "cat": "Logística", "pdf": "categorias.pdf"},
    {"nombre": "PS Bridge", "url": "https://ps-bridge.streamlit.app", "icon": "ps-bridge.svg", "desc": "Creación del fichero de subida de novedades a PrestaShop.", "color": "#e8eaf6", "cat": "Catálogo", "pdf": "bridge.pdf"},
    {"nombre": "Stock Amazon", "url": "https://stockamazon.streamlit.app", "icon": "stockamazon.svg", "desc": "Gestión de stock. Recuerda convertir el fichero primero.", "color": "#fffde7", "cat": "Stock", "has_step_prior": True, "prior_url": "https://convertirexcels.streamlit.app/", "pdf": "stock_amz.pdf"},
    {"nombre": "Seguimientos Amazon", "url": "https://seguimientosamazon.streamlit.app/", "icon": "stockamazon.svg", "desc": "Herramienta para el seguimiento y control de pedidos en Amazon.", "color": "#eceff1", "cat": "Logística", "pdf": "seguimiento.pdf"},
    {"nombre": "Amazon Facturas", "url": "https://transformarexcelamazonfacturas.streamlit.app/", "icon": "stockamazon.svg", "desc": "Transformación de ficheros Excel para facturación en Amazon.", "color": "#f3e5f5", "cat": "Facturación", "pdf": "facturas_amz.pdf"},
    {"nombre": "Dividir Excel", "url": "https://dividirexcel.streamlit.app/", "icon": "marketplaces.svg", "desc": "Herramienta para separar archivos Excel en múltiples pestañas.", "color": "#ede7f6", "cat": "Utilidad", "pdf": "dividir.pdf"},
    {"nombre": "Revisar URL Fotos", "url": "https://revisarurlimagenes.streamlit.app/", "icon": "marketplaces.svg", "desc": "Validación masiva de URLs de imágenes para evitar errores 404.", "color": "#fff8e1", "cat": "Calidad", "pdf": "urls_fotos.pdf"},
    {"nombre": "Actualiza URLs", "url": "https://actualizaurlsimagenes.streamlit.app/", "icon": "marketplaces.svg", "desc": "Edición y actualización masiva de rutas de imágenes en ficheros de carga.", "color": "#e0f7fa", "cat": "Catálogo", "pdf": "actualiza_urls.pdf"},
    {"nombre": "Comparar PS vs Amazon", "url": "https://compararpsvsamazon.streamlit.app/", "icon": "marketplaces.svg", "desc": "Auditoría de catálogo para detectar discrepancias entre PS y Amazon.", "color": "#e8f5e9", "cat": "Auditoría", "pdf": "comparador.pdf"},
    {"nombre": "Reviews Tracker", "url": "https://reviewstracker.streamlit.app", "icon": "marketplaces.svg", "desc": "Seguimiento y análisis de reseñas de clientes.", "color": "#f0f4c3", "cat": "Marketing", "pdf": "reviews.pdf"},
    {"nombre": "Unidad Nueva", "url": "https://unidadnueva.streamlit.app", "icon": "unidadnueva.svg", "desc": "Creación del fichero de subida a Cecopartners automatizado.", "color": "#fbe9e7", "cat": "Catálogo", "pdf": "unidad_nueva.pdf"},
    {"nombre": "Tipo Dispositivo", "url": "https://tipodispositivo.streamlit.app/", "icon": "marketplaces.svg", "desc": "Utilidad para identificar el tipo de dispositivo de acceso.", "color": "#f5f5f5", "cat": "Utilidad", "pdf": "dispositivo.pdf"},
    {"nombre": "Recortador Cadenas", "url": "https://recortadorcadenastexto.streamlit.app/", "icon": "marketplaces.svg", "desc": "Limitación de longitud de textos y limpieza de caracteres.", "color": "#eceff1", "cat": "Utilidad", "pdf": "recortador.pdf"}
]

# Estilos CSS
st.markdown("""
    <style>
    .card-title { color: #111; margin: 0; font-size: 1.3rem; font-weight: 800; line-height: 1.1; }
    .card-desc { color: #333; font-size: 0.95rem; margin-top: 10px; line-height: 1.3; font-weight: 500; height: 60px; overflow: hidden; }
    .app-card {
        padding: 20px; border-radius: 15px; border: 1px solid #e0e0e0;
        text-align: center; min-height: 330px; display: flex;
        flex-direction: column; justify-content: space-between; align-items: center; margin-bottom: 10px;
    }
    .pdf-link { margin-top: 10px; padding: 5px 10px; background: rgba(255,255,255,0.5); border-radius: 5px; }
    .intro-box {
        background-color: #f8f9fa; padding: 20px; border-radius: 15px; border-left: 5px solid #007bff; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Panel Central de Aplicaciones Turaco")

# SECCIÓN: EXPLICACIÓN
st.markdown("""
<div class="intro-box">
    <h4>📖 Centro de Operaciones y Estructuras</h4>
    <p style="font-size: 0.9rem;">Panel de control para la automatización de procesos. 
    Consulta los manuales <b>📂 Estructura PDF</b> para asegurar la validez de los ficheros de entrada.</p>
</div>
""", unsafe_allow_html=True)

search_query = st.text_input("🔍 Buscar aplicación...", "").lower()
apps_filtradas = [app for app in apps if search_query in app["nombre"].lower() or search_query in app["desc"].lower()]

# SECCIÓN: ÍNDICE EN TABLA
if not search_query:
    with st.expander("📊 Índice rápido y acceso directo", expanded=False):
        data_tabla = {
            "Aplicación": [f"[{a['nombre']}]({a['url']})" for a in apps],
            "Categoría": [a['cat'] for a in apps],
            "Función": [a['desc'] for a in apps]
        }
        st.table(data_tabla)

st.markdown("---")

# SECCIÓN: GRID DE TARJETAS
if apps_filtradas:
    cols = st.columns(4)
    for i, app in enumerate(apps_filtradas):
        with cols[i % 4]:
            b64_icon = get_svg_base64(f"iconos/{app['icon']}")
            icon_html = f'<img src="data:image/svg+xml;base64,{b64_icon}" width="50" style="margin-bottom:10px;"/>' if b64_icon else "🖼️"
            pdf_html = get_pdf_download_link(f"instrucciones/{app['pdf']}", "Estructura PDF")
            
            st.markdown(f"""
                <div class="app-card" style="background-color: {app['color']};">
                    <div>
                        {icon_html}
                        <div class="card-title">{app['nombre']}</div>
                        <div class="card-desc">{app['desc']}</div>
                    </div>
                    <div class="pdf-link">
                        {pdf_html}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            if app.get("has_step_prior"):
                c1, c2 = st.columns(2)
                with c1: st.link_button("❶ Conv", app['prior_url'], use_container_width=True)
                with c2: st.link_button("❷ Stock", app['url'], use_container_width=True)
            else:
                st.link_button("Abrir Aplicación", app['url'], use_container_width=True)
else:
    st.warning("No se encontraron coincidencias.")