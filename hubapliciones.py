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
    {"nombre": "Marketplaces", "url": "https://multitienda-bi-group.streamlit.app", "icon": "marketplaces.svg", "desc": "Business Intelligence de pedidos, análisis por marketplaces y año. Filtros comparativos mes a mes"},
    {"nombre": "50 Top Ventas ES", "url": "https://50topventases.streamlit.app", "icon": "50topventases.svg", "desc": "Creación del fichero para enviar el top ventas semanal de productos líderes en el mercado español."},
    {"nombre": "Actualizador Tarifas", "url": "https://actualizardortarifas.streamlit.app", "icon": "actualizardortarifas.svg", "desc": "Gestión y actualización de tarifas, sube la tarifa actual en xls y su actualización."},
    {"nombre": "Cecotec Downloader", "url": "https://cecotec-downloader.streamlit.app", "icon": "cecotec-downloader.svg", "desc": "Herramienta de descarga de catálogos y datos de las web de Cecotec por países."},
    {"nombre": "Features PS", "url": "https://featuresps.streamlit.app", "icon": "featuresps.svg", "desc": "Creación del fichero de subida de características técnicas en PrestaShop cruzando datos."},
    {"nombre": "Map Categories", "url": "https://mapcategories.streamlit.app", "icon": "mapcategories.svg", "desc": "Mapeo lógico y organización de categorías de productos Amazon vs PS."},
    {"nombre": "PS Bridge", "url": "https://ps-bridge.streamlit.app", "icon": "ps-bridge.svg", "desc": "Creación del fichero de subida de novedades a PrestaShop."},
    {
        "nombre": "Stock Amazon", 
        "url": "https://stockamazon.streamlit.app", 
        "icon": "stockamazon.svg", 
        "desc": "Actualización de stock en Amazon Seller. IMPORTANTE: Los ficheros deben ser .xlsx",
        "has_step_prior": True, # Marcador para lógica especial
        "prior_url": "https://convertirexcels.streamlit.app/",
        "prior_icon": "cecotec-downloader.svg" # Usamos el icono que pediste
    },
    {"nombre": "Unidad Nueva", "url": "https://unidadnueva.streamlit.app", "icon": "unidadnueva.svg", "desc": "Creación del fichero de subida a Cecopartners de pedidos automatizado"}
]

# --- INTERFAZ ---
st.title("🚀 Panel Central de Aplicaciones")

search_query = st.text_input("🔍 Buscar aplicación por nombre o descripción...", "").lower()

apps_filtradas = [
    app for app in apps 
    if search_query in app["nombre"].lower() or search_query in app["desc"].lower()
]

st.markdown("---")

if apps_filtradas:
    cols = st.columns(3)
    for i, app in enumerate(apps_filtradas):
        with cols[i % 3]:
            with st.container(border=True):
                # Renderizar icono principal
                svg_html = render_svg(f"iconos/{app['icon']}")
                if svg_html:
                    st.markdown(svg_html, unsafe_allow_html=True)
                else:
                    st.markdown("<h1 style='text-align: center;'>🖼️</h1>", unsafe_allow_html=True)
                
                st.subheader(app['nombre'])
                st.write(app['desc'])
                
                # Lógica especial para Amazon + Convertidor
                if app.get("has_step_prior"):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.link_button("1. Convertir Excel", app['prior_url'], use_container_width=True, type="secondary")
                    with c2:
                        st.link_button("2. Abrir Stock", app['url'], use_container_width=True, type="primary")
                else:
                    st.link_button("Abrir Aplicación", app['url'], use_container_width=True)
else:
    st.warning("No se encontraron aplicaciones.")

# Estética
st.markdown("""
    <style>
    .stButton button { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)