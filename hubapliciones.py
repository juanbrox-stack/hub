import streamlit as st
import base64
import pandas as pd

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

# LISTA COMPLETA DE APPS (21 aplicaciones)
apps = [
    {"nombre": "Marketplaces", "url": "https://multitienda-bi-group.streamlit.app", "icon": "marketplaces.svg", "desc": "Business Intelligence de pedidos, análisis por marketplaces y año.", "color": "#e3f2fd", "cat": "BI & Ventas"},
    {"nombre": "50 Top Ventas ES", "url": "https://50topventases.streamlit.app", "icon": "50topventases.svg", "desc": "Creación del fichero para enviar el top ventas semanal de productos líderes.", "color": "#f1f8e9", "cat": "Reporting"},
    {"nombre": "Actualizador Tarifas", "url": "https://actualizardortarifas.streamlit.app", "icon": "actualizardortarifas.svg", "desc": "Gestión y actualización de tarifas, genera el fichero con la tarifa completa.", "color": "#fff3e0", "cat": "Tarifas"},
    {"nombre": "Cecotec Downloader", "url": "https://cecotec-downloader.streamlit.app", "icon": "cecotec-downloader.svg", "desc": "Herramienta de descarga de catálogos y datos de las web de Cecotec.", "color": "#f3e5f5", "cat": "Scraping"},
    {"nombre": "Features PS", "url": "https://featuresps.streamlit.app", "icon": "featuresps.svg", "desc": "Creación del fichero de subida de características técnicas en PrestaShop.", "color": "#efebe9", "cat": "Catálogo"},
    {"nombre": "Características 2026", "url": "https://caracteristicaspsturaco2026.streamlit.app/", "icon": "featuresps.svg", "desc": "Nueva utilidad 2026 para la gestión avanzada de características en PrestaShop.", "color": "#e1f5fe", "cat": "Catálogo"},
    {"nombre": "Errors", "url": "https://errors.streamlit.app/", "icon": "marketplaces.svg", "desc": "Analizar errores de publicación en marketplaces. Subir fichero de Mirakl.", "color": "#ffebee", "cat": "Errores"},
    {"nombre": "Errores BeezUP", "url": "https://erroresbeezup.streamlit.app/", "icon": "marketplaces.svg", "desc": "Analizador y gestor de errores de publicación específicos de BeezUP.", "color": "#fff3e0", "cat": "Errores"},
    {"nombre": "Variaciones Cdiscount", "url": "https://variacionescdiscount.streamlit.app/", "icon": "marketplaces.svg", "desc": "Generador de variaciones y combinaciones específicas para Cdiscount.", "color": "#fce4ec", "cat": "Catálogo"},
    {"nombre": "Map Categories", "url": "https://mapcategories.streamlit.app", "icon": "mapcategories.svg", "desc": "Mapeo lógico y organización de categorías Amazon vs PS.", "color": "#e0f2f1", "cat": "Logística"},
    {"nombre": "PS Bridge", "url": "https://ps-bridge.streamlit.app", "icon": "ps-bridge.svg", "desc": "Creación del fichero de subida de novedades a PrestaShop.", "color": "#e8eaf6", "cat": "Catálogo"},
    {"nombre": "Stock Amazon", "url": "https://stockamazon.streamlit.app", "icon": "stockamazon.svg", "desc": "Gestión de stock. Recuerda convertir el fichero primero.", "color": "#fffde7", "cat": "Stock", "has_step_prior": True, "prior_url": "https://convertirexcels.streamlit.app/"},
    {"nombre": "Seguimientos Amazon", "url": "https://seguimientosamazon.streamlit.app/", "icon": "stockamazon.svg", "desc": "Herramienta para el seguimiento y control de pedidos en Amazon.", "color": "#eceff1", "cat": "Logística"},
    {"nombre": "Amazon Facturas", "url": "https://transformarexcelamazonfacturas.streamlit.app/", "icon": "stockamazon.svg", "desc": "Transformación de ficheros Excel para facturación en Amazon.", "color": "#f3e5f5", "cat": "Facturación"},
    {"nombre": "Dividir Excel", "url": "https://dividirexcel.streamlit.app/", "icon": "marketplaces.svg", "desc": "Herramienta para separar archivos Excel en múltiples pestañas.", "color": "#ede7f6", "cat": "Utilidad"},
    {"nombre": "Revisar URL Fotos", "url": "https://revisarurlimagenes.streamlit.app/", "icon": "marketplaces.svg", "desc": "Validación masiva de URLs de imágenes para evitar errores 404.", "color": "#fff8e1", "cat": "Calidad"},
    {"nombre": "Comparar PS vs Amazon", "url": "https://compararpsvsamazon.streamlit.app/", "icon": "marketplaces.svg", "desc": "Auditoría de catálogo para detectar discrepancias entre PS y Amazon.", "color": "#e8f5e9", "cat": "Auditoría"},
    {"nombre": "Reviews Tracker", "url": "https://reviewstracker.streamlit.app", "icon": "marketplaces.svg", "desc": "Seguimiento y análisis de reseñas de clientes.", "color": "#f0f4c3", "cat": "Marketing"},
    {"nombre": "Unidad Nueva", "url": "https://unidadnueva.streamlit.app", "icon": "unidadnueva.svg", "desc": "Creación del fichero de subida a Cecopartners automatizado.", "color": "#fbe9e7", "cat": "Catálogo"},
    {"nombre": "Tipo Dispositivo", "url": "https://tipodispositivo.streamlit.app/", "icon": "marketplaces.svg", "desc": "Utilidad para identificar el tipo de dispositivo de acceso.", "color": "#f5f5f5", "cat": "Utilidad"},
    {"nombre": "Recortador Cadenas", "url": "https://recortadorcadenastexto.streamlit.app/", "icon": "marketplaces.svg", "desc": "Limitación de longitud de textos y limpieza de caracteres.", "color": "#eceff1", "cat": "Utilidad"}
]

# Estilos CSS
st.markdown("""
    <style>
    .card-title { color: #111; margin: 0; font-size: 1.4rem; font-weight: 800; line-height: 1.1; }
    .card-desc { color: #333; font-size: 1rem; margin-top: 15px; line-height: 1.4; font-weight: 500; }
    .app-card {
        padding: 20px; border-radius: 15px; border: 1px solid #e0e0e0;
        text-align: center; min-height: 310px; display: flex;
        flex-direction: column; justify-content: center; align-items: center; margin-bottom: 10px;
    }
    .intro-box {
        background-color: #f8f9fa; padding: 25px; border-radius: 15px;
        border-left: 5px solid #007bff; margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Panel Central de Aplicaciones Turaco")

# --- SECCIÓN: EXPLICACIÓN DEL PANEL ---
st.markdown("""
<div class="intro-box">
    <h3>📖 Sobre este ecosistema</h3>
    <p>Este panel centraliza las herramientas de automatización diseñadas para optimizar el flujo de trabajo en marketplaces. 
    El objetivo principal es <b>eliminar errores manuales</b> y <b>reducir tiempos de proceso</b> mediante:</p>
    <ul>
        <li><b>Gestión de Catálogo:</b> Preparación de ficheros masivos para PrestaShop y Marketplaces.</li>
        <li><b>Control de Errores:</b> Auditores de publicación para Mirakl y Amazon.</li>
        <li><b>Inteligencia de Datos:</b> Transformación de reportes de ventas y facturación en información útil.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

search_query = st.text_input("🔍 Buscar aplicación por nombre o funcionalidad...", "").lower()

# Filtrar aplicaciones
apps_filtradas = [app for app in apps if search_query in app["nombre"].lower() or search_query in app["desc"].lower()]

# --- SECCIÓN: ÍNDICE EN TABLA ---
if not search_query:
    with st.expander("📊 Índice rápido de utilidades (Acceso directo)", expanded=True):
        # Crear DataFrame para la tabla
        data_tabla = {
            "Aplicación": [f"[{a['nombre']}]({a['url']})" for a in apps],
            "Categoría": [a['cat'] for a in apps],
            "Utilidad Principal": [a['desc'] for a in apps]
        }
        st.table(data_tabla)

st.markdown("---")

# --- SECCIÓN: GRID DE TARJETAS ---
if apps_filtradas:
    cols = st.columns(4)
    for i, app in enumerate(apps_filtradas):
        with cols[i % 4]:
            b64_icon = get_svg_base64(f"iconos/{app['icon']}")
            icon_html = f'<img src="data:image/svg+xml;base64,{b64_icon}" width="55" style="margin-bottom:12px;"/>' if b64_icon else "🖼️"
            
            st.markdown(f"""
                <div class="app-card" style="background-color: {app['color']};">
                    {icon_html}
                    <div class="card-title">{app['nombre']}</div>
                    <div class="card-desc">{app['desc']}</div>
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