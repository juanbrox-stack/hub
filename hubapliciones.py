import streamlit as st
import base64

# Configuración de página
st.set_page_config(page_title="Hub de Aplicaciones", layout="wide", page_icon="🚀")

def render_svg(svg_path):
    """Convierte un archivo SVG local en una etiqueta HTML img en base64."""
    try:
        with open(svg_path, "r") as f:
            svg = f.read()
            b64 = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
            return f'<img src="data:image/svg+xml;base64,{b64}" width="80" style="display: block; margin: auto;"/>'
    except FileNotFoundError:
        return None

# Datos de las aplicaciones
apps = [
    {"nombre": "Marketplaces", "url": "https://multitienda-bi-group.streamlit.app", "icon": "marketplaces.svg", "desc": "Gestión centralizada de múltiples tiendas y Business Intelligence."},
    {"nombre": "50 Top Ventas ES", "url": "https://50topventases.streamlit.app", "icon": "50topventases.svg", "desc": "Análisis de productos líderes en el mercado español."},
    {"nombre": "Actualizador Tarifas", "url": "https://actualizardortarifas.streamlit.app", "icon": "actualizardortarifas.svg", "desc": "Gestión y actualización masiva de precios y tarifas."},
    {"nombre": "Cecotec Downloader", "url": "https://cecotec-downloader.streamlit.app", "icon": "cecotec-downloader.svg", "desc": "Herramienta de descarga de catálogos y datos Cecotec."},
    {"nombre": "Features PS", "url": "https://featuresps.streamlit.app", "icon": "featuresps.svg", "desc": "Administración de características técnicas en PrestaShop."},
    {"nombre": "Map Categories", "url": "https://mapcategories.streamlit.app", "icon": "mapcategories.svg", "desc": "Mapeo lógico y organización de categorías de productos."},
    {"nombre": "PS Bridge", "url": "https://ps-bridge.streamlit.app", "icon": "ps-bridge.svg", "desc": "Sincronización y puente de datos entre sistemas y PrestaShop."},
    {"nombre": "Stock Amazon", "url": "https://stockamazon.streamlit.app", "icon": "stockamazon.svg", "desc": "Control de inventario y disponibilidad en Amazon Seller."},
    {"nombre": "Unidad Nueva", "url": "https://unidadnueva.streamlit.app", "icon": "unidadnueva.svg", "desc": "Configuración y alta de nuevas unidades de negocio."}
]

# --- INTERFAZ ---
st.title("🚀 Panel Central de Aplicaciones")

# Barra de búsqueda
search_query = st.text_input("🔍 Buscar aplicación por nombre o descripción...", "").lower()

# Filtrado lógico
apps_filtradas = [
    app for app in apps 
    if search_query in app["nombre"].lower() or search_query in app["desc"].lower()
]

st.markdown("---")

# Renderizado de la cuadrícula
if apps_filtradas:
    cols = st.columns(3)
    for i, app in enumerate(apps_filtradas):
        with cols[i % 3]:
            with st.container(border=True):
                # Renderizar icono SVG
                svg_html = render_svg(f"iconos/{app['icon']}")
                if svg_html:
                    st.markdown(svg_html, unsafe_allow_html=True)
                else:
                    st.center("🖼️") # Placeholder si falta el archivo
                
                st.subheader(app['nombre'])
                st.write(app['desc'])
                
                # Botón con link
                st.link_button("Abrir Aplicación", app['url'], use_container_width=True)
else:
    st.warning("No se encontraron aplicaciones que coincidan con tu búsqueda.")

# Estética adicional
st.markdown("""
    <style>
    .stButton button { border-radius: 20px; border: 1px solid #007bff; }
    div[data-testid="stExpander"] { border: none; }
    </style>
    """, unsafe_allow_html=True)