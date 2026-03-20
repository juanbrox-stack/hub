import streamlit as st
import base64

# Configuración de página
st.set_page_config(page_title="Hub de Aplicaciones", layout="wide", page_icon="🚀")

def get_svg_base64(svg_path):
    """Obtiene el base64 de un SVG para insertarlo en el HTML."""
    try:
        with open(svg_path, "r") as f:
            svg = f.read()
            return base64.b64encode(svg.encode('utf-8')).decode('utf-8')
    except FileNotFoundError:
        return None

# Datos de las aplicaciones
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

# Estilos CSS globales (Botones azules y fuentes)
st.markdown("""
    <style>
    div.stButton > button {
        background-color: #007bff !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        height: 3em !important;
        width: 100% !important;
        font-weight: bold !important;
    }
    div.stButton > button:hover {
        background-color: #0056b3 !important;
        border: none !important;
    }
    /* Estilo para las tarjetas */
    .app-card {
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #e0e0e0;
        text-align: center;
        margin-bottom: 10px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
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
            # Encabezado de la tarjeta con color e icono
            b64_icon = get_svg_base64(f"iconos/{app['icon']}")
            icon_html = f'<img src="data:image/svg+xml;base64,{b64_icon}" width="70" style="margin-bottom:15px;"/>' if b64_icon else "🖼️"
            
            # Dibujamos el contenedor de color que incluye el texto
            st.markdown(f"""
                <div class="app-card" style="background-color: {app['color']};">
                    <div style="flex-grow: 1;">
                        {icon_html}
                        <h3 style="color: #333; margin-top:0;">{app['nombre']}</h3>
                        <p style="color: #555; font-size: 0.9rem; min-height: 60px;">{app['desc']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Los botones se ponen justo debajo del markdown dentro de la misma columna
            if app.get("has_step_prior"):
                c1, c2 = st.columns(2)
                with c1:
                    st.link_button("❶ Convertir", app['prior_url'], use_container_width=True)
                with c2:
                    st.link_button("❷ Stock", app['url'], use_container_width=True)
            else:
                st.link_button("Abrir Aplicación", app['url'], use_container_width=True)
else:
    st.warning("No se encontraron coincidencias.")