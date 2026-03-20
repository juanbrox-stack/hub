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
            return f'<img src="data:image/svg+xml;base64,{b64}" width="70" style="display: block; margin: auto; padding-bottom: 10px;"/>'
    except FileNotFoundError:
        return None

# Datos de las aplicaciones con colores asignados
apps = [
    {"nombre": "Marketplaces", "url": "https://multitienda-bi-group.streamlit.app", "icon": "marketplaces.svg", "desc": "Business Intelligence de pedidos, análisis por marketplaces y año.", "color": "#e3f2fd"},
    {"nombre": "50 Top Ventas ES", "url": "https://50topventases.streamlit.app", "icon": "50topventases.svg", "desc": "Creación del fichero para enviar el top ventas semanal de productos líderes.", "color": "#f1f8e9"},
    {"nombre": "Actualizador Tarifas", "url": "https://actualizardortarifas.streamlit.app", "icon": "actualizardortarifas.svg", "desc": "Gestión y actualización de tarifas, genera el fichero con la tarifa completa.", "color": "#fff3e0"},
    {"nombre": "Cecotec Downloader", "url": "https://cecotec-downloader.streamlit.app", "icon": "cecotec-downloader.svg", "desc": "Herramienta de descarga de catálogos y datos de las web de Cecotec.", "color": "#f3e5f5"},
    {"nombre": "Features PS", "url": "https://featuresps.streamlit.app", "icon": "featuresps.svg", "desc": "Creación del fichero de subida de características técnicas en PrestaShop.", "color": "#efebe9"},
    {"nombre": "Map Categories", "url": "https://mapcategories.streamlit.app", "icon": "mapcategories.svg", "desc": "Mapeo lógico y organización de categorías Amazon vs PS.", "color": "#e0f2f1"},
    {"nombre": "PS Bridge", "url": "https://ps-bridge.streamlit.app", "icon": "ps-bridge.svg", "desc": "Creación del fichero de subida de novedades a PrestaShop.", "color": "#e8eaf6"},
    {
        "nombre": "Stock Amazon", 
        "url": "https://stockamazon.streamlit.app", 
        "icon": "stockamazon.svg", 
        "desc": "Gestión de stock. Recuerda convertir el fichero primero si no es .xlsx",
        "color": "#fffde7",
        "has_step_prior": True,
        "prior_url": "https://convertirexcels.streamlit.app/"
    },
    {"nombre": "Unidad Nueva", "url": "https://unidadnueva.streamlit.app", "icon": "unidadnueva.svg", "desc": "Creación del fichero de subida a Cecopartners de pedidos automatizado.", "color": "#fbe9e7"}
]

# Estilos CSS personalizados
st.markdown("""
    <style>
    /* Estilo general de los botones */
    .stButton button {
        background-color: #007bff !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        transition: 0.3s;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #0056b3 !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    /* Estilo para el botón secundario (Paso 1) */
    div[data-testid="stHorizontalBlock"] .stButton button {
        font-size: 0.8rem;
    }
    /* Quitar bordes por defecto de Streamlit */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Panel Central de Aplicaciones")
search_query = st.text_input("🔍 Buscar aplicación...", "").lower()

apps_filtradas = [app for app in apps if search_query in app["nombre"].lower() or search_query in app["desc"].lower()]

st.markdown("---")

if apps_filtradas:
    cols = st.columns(3)
    for i, app in enumerate(apps_filtradas):
        with cols[i % 3]:
            # Aplicamos el color de fondo personalizado usando una división HTML
            st.markdown(f"""
                <div style="background-color: {app['color']}; padding: 20px; border-radius: 15px; border: 1px solid #ddd; height: 350px; margin-bottom: 20px;">
                """, unsafe_allow_html=True)
            
            svg_html = render_svg(f"iconos/{app['icon']}")
            if svg_html:
                st.markdown(svg_html, unsafe_allow_html=True)
            
            st.markdown(f"<h3 style='text-align: center; color: #333;'>{app['nombre']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; color: #666; font-size: 0.9rem;'>{app['desc']}</p>", unsafe_allow_html=True)
            
            if app.get("has_step_prior"):
                c1, c2 = st.columns(2)
                with c1:
                    st.link_button("❶ Convertir", app['prior_url'], use_container_width=True)
                with c2:
                    st.link_button("❷ Stock", app['url'], use_container_width=True)
            else:
                st.link_button("Abrir Aplicación", app['url'], use_container_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
else:
    st.warning("No se encontraron coincidencias.")