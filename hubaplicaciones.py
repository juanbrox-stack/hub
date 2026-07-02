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

# --- LISTA COMPLETA DE APPS GENERALES (Orden Alfabético - Apps agrupadas en flujos excluidas para evitar duplicados) ---
apps = [
    {"nombre": "Amazon Bulk Master", "url": "https://rellenaplantillasamazon.streamlit.app/", "icon": "stockamazon.svg", "desc": "Rellena plantillas de Amazon de forma masiva y automatizada.", "color": "#FAF9F5", "cat": "Catálogo", "pdf": "Manual_Amazon_Bulk_Master_v101_es-ES.pdf"},
    {"nombre": "Amazon Facturas", "url": "https://transformarexcelamazonfacturas.streamlit.app/", "icon": "stockamazon.svg", "desc": "Transformación de ficheros para facturación Amazon.", "color": "#FAF9F5", "cat": "Facturación", "pdf": "Amazon Facturas.pdf"},
    {"nombre": "Calculadora ROI Automatización", "url": "https://calculadoraretornoinversion.streamlit.app/", "icon": "marketplaces.svg", "desc": "Calcula el ahorro y rentabilidad de proyectos de automatización.", "color": "#FAF9F5", "cat": "Utilidad", "pdf": "Calculadora_ROI_Automatizacion.pdf"},
    {"nombre": "Cecotec Downloader", "url": "https://cecotec-downloader.streamlit.app", "icon": "cecotec-downloader.svg", "desc": "Descarga de catálogos y datos de la web de Cecotec.", "color": "#FAF9F5", "cat": "Scraping", "pdf": "Cecotec Downloader.pdf"},
    {"nombre": "Comisiones MediaMarkt", "url": "https://comisionesmediamarkt.streamlit.app/", "icon": "marketplaces.svg", "desc": "Cálculo y desglose de comisiones para el marketplace de MediaMarkt.", "color": "#FAF9F5", "cat": "Facturación", "pdf": "Manual_Comisiones_MediaMarkt_v12.pdf"},
    {"nombre": "Dividir Excel", "url": "https://dividirexcel.streamlit.app/", "icon": "marketplaces.svg", "desc": "Separa archivos Excel en múltiples pestañas o ficheros.", "color": "#FAF9F5", "cat": "Utilidad", "pdf": "Dividir Excel.pdf"},
    {"nombre": "Informe Ventas MKT", "url": "https://automatizacionventasmkt.streamlit.app/", "icon": "marketplaces.svg", "desc": "Análisis estratégico y automatización de informes para el departamento de Marketing.", "color": "#FAF9F5", "cat": "Marketing", "pdf": "Manual_Usuario_Informe_Ventas_MKT.pdf"},
    {"nombre": "InformeSeller", "url": "https://informeseller.streamlit.app/", "icon": "marketplaces.svg", "desc": "Generación de informes detallados de ventas y rendimiento Seller.", "color": "#FAF9F5", "cat": "BI", "pdf": "InformeSeller.pdf"},
    {"nombre": "Marketplaces", "url": "https://multitienda-bi-group.streamlit.app", "icon": "marketplaces.svg", "desc": "BI de pedidos, análisis por marketplaces y año.", "color": "#FAF9F5", "cat": "BI", "pdf": "Marketplaces.pdf"},
    {"nombre": "Recortador Cadenas", "url": "https://recortadorcadenastexto.streamlit.app/", "icon": "marketplaces.svg", "desc": "Limpieza y recorte de longitud de textos.", "color": "#FAF9F5", "cat": "Utilidad", "pdf": "Recortador Cadenas.pdf"},
    {"nombre": "Reviews Tracker", "url": "https://reviewstracker.streamlit.app", "icon": "marketplaces.svg", "desc": "Seguimiento y análisis de reseñas de clientes.", "color": "#FAF9F5", "cat": "Marketing", "pdf": "Reviews Tracker.pdf"},
    {"nombre": "Seguimientos Amazon", "url": "https://seguimientosamazon.streamlit.app/", "icon": "stockamazon.svg", "desc": "Seguimiento y control de pedidos en Amazon.", "color": "#FAF9F5", "cat": "Logística", "pdf": "Seguimientos Amazon.pdf"},
    {"nombre": "SellerFlex FR", "url": "https://sellerflexfr.streamlit.app/", "icon": "marketplaces.svg", "desc": "Gestión y optimización de envíos a través de SellerFlex para Francia.", "color": "#FAF9F5", "cat": "Logística", "pdf": "Manual_Usuario_SellerFlex_FR.pdf"},
    {"nombre": "Tipo Dispositivo", "url": "https://tipodispositivo.streamlit.app/", "icon": "marketplaces.svg", "desc": "Identificación del tipo de dispositivo de acceso.", "color": "#FAF9F5", "cat": "Utilidad", "pdf": "Tipo Dispositivo.pdf"},
    {"nombre": "Unidad Nueva", "url": "https://unidadnueva.streamlit.app", "icon": "unidadnueva.svg", "desc": "Subida a Cecopartners de pedidos automatizada.", "color": "#FAF9F5", "cat": "Catálogo", "pdf": "Unidad Nueva.pdf"},
    {"nombre": "Variaciones Cdiscount", "url": "https://variacionescdiscount.streamlit.app/", "icon": "marketplaces.svg", "desc": "Generador de variaciones específicas para Cdiscount.", "color": "#FAF9F5", "cat": "Catálogo", "pdf": "Variaciones Cdiscount.pdf"}
]

# --- FLUJO SECUENCIAL 1: GESTIÓN DE PEDIDOS CECOTEC ---
flujo_apps = [
    {"nombre": "❶ Volcar Pedidos Cecotec", "url": "https://volcarpedidos.streamlit.app/", "icon": "marketplaces.svg", "desc": "Automatización para el volcado masivo e integración de pedidos.", "pdf": "Manual_Usuario_Volcar_Pedidos_Cecotec.pdf"},
    {"nombre": "❷ Buscar Sustituto", "url": "https://buscarsustituto.streamlit.app/", "icon": "marketplaces.svg", "desc": "Localización y asignación de referencias alternativas de stock.", "pdf": "Buscar_Sustituto.pdf"},
    {"nombre": "❸ Borradores Cecopartners", "url": "https://borradorescecopartners.streamlit.app/", "icon": "marketplaces.svg", "desc": "Generación final y carga de borradores en la plataforma Cecopartners.", "pdf": "Borradores_Cecopartners.pdf"}
]

# --- FLUJO SECUENCIAL 2: PLYTIX -> PRESTASHOP ---
flujo2_apps = [
    {"nombre": "❶ Plytix Downloader", "url": "https://descargaspim.streamlit.app/", "icon": "marketplaces.svg", "desc": "Descarga masiva de activos y datos desde el PIM Plytix.", "pdf": "manual_plytix_downloader.pdf"},
    {"nombre": "❷ PS Bridge", "url": "https://ps-bridge.streamlit.app", "icon": "ps-bridge.svg", "desc": "Fichero de subida de novedades a PrestaShop.", "pdf": "PS Bridge.pdf"}
]

# --- FLUJO SECUENCIAL 3: TARIFAS ---
flujo3_apps = [
    {"nombre": "❶ Actualizador Tarifas", "url": "https://actualizardortarifas.streamlit.app", "icon": "actualizardortarifas.svg", "desc": "Gestión y actualización de tarifas, genera el fichero completo.", "pdf": "Actualizador Tarifas.pdf"},
    {"nombre": "❷ Actualizador Tarifas Herramientas", "url": "https://creaficherostarifasherramientas.streamlit.app/", "icon": "actualizardortarifas.svg", "desc": "Generador y actualizador automatizado de ficheros de tarifas de herramientas.", "pdf": "Manual_de_Usuario_Actualizador_Tarifas.pdf"},
    {"nombre": "❸ Generador Tarifas Amazon", "url": "https://generarplantillatarifasamazon.streamlit.app/", "icon": "stockamazon.svg", "desc": "Generación de plantillas de tarifas personalizadas para Amazon.", "pdf": "Manual_Generador_Tarifas_Amazon.pdf"}
]

# --- FLUJO SECUENCIAL 4: URLs / IMÁGENES PARA PRESTASHOP ---
flujo4_apps = [
    {"nombre": "❶ Extractor de URLs para PrestaShop", "url": "https://concatenarurl.streamlit.app/", "icon": "marketplaces.svg", "desc": "Generador de URLs absolutas para imágenes de productos.", "pdf": "Extractor de URLs para PrestaShop.pdf"},
    {"nombre": "❷ Actualiza URLs", "url": "https://actualizaurlsimagenes.streamlit.app/", "icon": "marketplaces.svg", "desc": "Edición masiva de rutas de imágenes en ficheros.", "pdf": "Actualiza URLs.pdf"},
    {"nombre": "❸ Revisar URL Fotos", "url": "https://revisarurlimagenes.streamlit.app/", "icon": "marketplaces.svg", "desc": "Validación masiva de URLs de imágenes (Evita 404).", "pdf": "Revisar URL Fotos.pdf"}
]

# --- FLUJO SECUENCIAL 5: AUDITORÍA DE CATÁLOGO ---
flujo5_apps = [
    {"nombre": "❶ Comparar PS vs Amazon", "url": "https://compararpsvsamazon.streamlit.app/", "icon": "marketplaces.svg", "desc": "Auditoría de catálogo PrestaShop vs Amazon.", "pdf": "Comparar PS vs Amazon.pdf"},
    {"nombre": "❷ Comparador Bestseller", "url": "https://comparadorbestseller.streamlit.app/", "icon": "marketplaces.svg", "desc": "Herramienta avanzada de comparación y auditoría para productos Bestseller.", "pdf": "Manual_Usuario_Comparador_Bestseller_v3.pdf"},
    {"nombre": "❸ SKUs Faltantes Amazon", "url": "https://skusfaltantesamazon.streamlit.app/", "icon": "stockamazon.svg", "desc": "Auditoría y comparativa de productos creados para la detección de SKUs faltantes en Amazon.", "pdf": "ManualCompartivaProductosCreadosAmazonJabiruTuraco.pdf"}
]

# --- FLUJO SECUENCIAL 6: STOCK AMAZON ---
flujo6_apps = [
    {"nombre": "❶ Convertir Excel", "url": "https://convertirexcels.streamlit.app/", "icon": "marketplaces.svg", "desc": "Conversión de ficheros a formato .xlsx antes de gestionar el stock.", "pdf": "Convertir Excel.pdf"},
    {"nombre": "❷ Stock Amazon", "url": "https://stockamazon.streamlit.app", "icon": "stockamazon.svg", "desc": "Gestión de stock una vez convertido el fichero a .xlsx.", "pdf": "Stock Amazon.pdf"},
    {"nombre": "❸ Control Desactivados", "url": "https://controldesactivados.streamlit.app/", "icon": "marketplaces.svg", "desc": "Auditoría y control de activación para stock deshabilitado tras la gestión.", "pdf": "Manual_Control_Activacion_Stock.pdf"}
]

# --- FLUJO SECUENCIAL 7: ERRORES ---
flujo7_apps = [
    {"nombre": "❶ Errors", "url": "https://errors.streamlit.app/", "icon": "marketplaces.svg", "desc": "Analizar errores de publicación Mirakl / Marketplaces.", "pdf": "Errors.pdf"},
    {"nombre": "❷ Errores BeezUP", "url": "https://erroresbeezup.streamlit.app/", "icon": "marketplaces.svg", "desc": "Gestor de errores de publicación específicos de BeezUP.", "pdf": "Errores BeezUP.pdf"}
]

# --- FLUJO SECUENCIAL 8: CATEGORÍAS / FEATURES PRESTASHOP ---
flujo8_apps = [
    {"nombre": "❶ Map Categories", "url": "https://mapcategories.streamlit.app", "icon": "mapcategories.svg", "desc": "Mapeo lógico de categorías Amazon vs PrestaShop.", "pdf": "Map Categories.pdf"},
    {"nombre": "❷ MM Category Explorer", "url": "https://atributosmediamarkt.streamlit.app/", "icon": "marketplaces.svg", "desc": "Explorador de categorías y atributos específicos para MediaMarkt.", "pdf": "Manual_MM_Category_Explorer.pdf"},
    {"nombre": "❸ Features PS", "url": "https://featuresps.streamlit.app", "icon": "featuresps.svg", "desc": "Creación de fichero de características técnicas PrestaShop.", "pdf": "Features PS.pdf"},
    {"nombre": "❹ Características 2026", "url": "https://caracteristicaspsturaco2026.streamlit.app/", "icon": "featuresps.svg", "desc": "Gestión avanzada de características PrestaShop 2026.", "pdf": "Características 2026.pdf"}
]

TODOS_LOS_FLUJOS = [
    ("Flujo de Trabajo Secuencial: Gestión de Pedidos Cecotec", flujo_apps, "flujo1"),
    ("Flujo de Trabajo Secuencial: Plytix a PrestaShop", flujo2_apps, "flujo2"),
    ("Flujo de Trabajo Secuencial: Tarifas", flujo3_apps, "flujo3"),
    ("Flujo de Trabajo Secuencial: URLs e Imágenes para PrestaShop", flujo4_apps, "flujo4"),
    ("Flujo de Trabajo Secuencial: Auditoría de Catálogo", flujo5_apps, "flujo5"),
    ("Flujo de Trabajo Secuencial: Stock Amazon", flujo6_apps, "flujo6"),
    ("Flujo de Trabajo Secuencial: Errores", flujo7_apps, "flujo7"),
    ("Flujo de Trabajo Secuencial: Categorías y Features PrestaShop", flujo8_apps, "flujo8"),
]

# Estilos CSS
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* Forzar visibilidad Buscador */
    [data-testid="stTextInput"] label p { color: #ffffff !important; font-weight: bold; }
    [data-testid="stTextInput"] input { 
        color: #ffffff !important; 
        background-color: #1a1a1a !important; 
        border: 1px solid #333 !important;
    }

    /* Forzar visibilidad Índice (Expander) */
    .stExpander { background-color: #000000 !important; border: 1px solid #333 !important; }
    .stExpander [data-testid="stHeader"] p { color: #ffffff !important; font-weight: bold; }
    .stExpander [data-testid="stExpanderDetails"] { background-color: #000000 !important; }
    
    table { background-color: #000000 !important; color: #ffffff !important; }
    th { color: #3EB1C8 !important; }

    /* Tarjetas Cream */
    .card-title { color: #111111 !important; margin: 0; font-size: 1.15rem; font-weight: 800; line-height: 1.1; }
    .card-desc { color: #333333 !important; font-size: 0.85rem; margin-top: 5px; line-height: 1.2; font-weight: 500; }
    .app-card {
        padding: 12px 15px; border-radius: 12px; border: 1px solid #333;
        text-align: center; min-height: 145px; display: flex;
        flex-direction: column; justify-content: center; align-items: center; margin-bottom: 10px;
        background-color: #FAF9F5;
    }

    /* Contenedor Visual del Flujo */
    .workflow-container {
        background-color: #111111;
        padding: 20px;
        border-radius: 15px;
        border: 2px dashed #3EB1C8;
        margin: 20px 0;
    }
    .workflow-title {
        color: #3EB1C8 !important;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 15px;
        text-align: left;
    }
    .flow-arrow {
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 2rem;
        color: #3EB1C8;
        height: 145px;
    }

    /* Botonera General Turquesa */
    [data-testid="stVerticalBlock"] > div:has(div.stButton), 
    [data-testid="stVerticalBlock"] > div:has(div.stDownloadButton),
    [data-testid="stVerticalBlock"] > div:has(div.stLinkButton) {
        display: flex; justify-content: center; width: 100%;
    }

    div.stButton > button, div.stDownloadButton > button, div.stLinkButton > a {
        background-color: #3EB1C8 !important; 
        color: #E0E0E0 !important;
        border-radius: 8px !important; 
        font-weight: 800 !important; 
        font-size: 0.82rem !important; 
        height: 3em !important; 
        width: 160px !important; 
        margin: 5px auto !important; 
        border: none !important; 
        display: flex !important; 
        justify-content: center !important; 
        align-items: center !important;
        text-align: center !important; 
        line-height: 1.2 !important;   
        text-decoration: none !important; 
        transition: all 0.3s ease;
    }
    
    div.stButton > button:hover, div.stDownloadButton > button:hover, div.stLinkButton > a:hover {
        background-color: #359fb4 !important; 
        color: #ffffff !important;
        border: none !important;
    }

    /* Caja de Contenedor Superior */
    .top-priority-container {
        background-color: #141414; 
        padding: 15px; 
        border-radius: 10px; 
        border: 1px solid #222; 
        min-height: 80px; 
        display: flex; 
        align-items: center;
    }

    .intro-box { background-color: #1a1a1a; padding: 12px; border-radius: 10px; border-left: 5px solid #3EB1C8; margin-bottom: 15px; }
    a { color: #3EB1C8 !important; text-decoration: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

def render_flujo(titulo, flujo_list, key_prefix):
    """Renderiza un bloque de flujo secuencial dentro del marco turquesa punteado."""
    st.markdown(f'<div class="workflow-container"><div class="workflow-title">🔄 {titulo}</div>', unsafe_allow_html=True)

    n = len(flujo_list)
    col_spec, indices, arrows = [], [], []
    for i in range(n):
        indices.append(len(col_spec))
        col_spec.append(3)
        if i < n - 1:
            arrows.append(len(col_spec))
            col_spec.append(0.5)

    cols = st.columns(col_spec)

    for idx, app in enumerate(flujo_list):
        with cols[indices[idx]]:
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

            pdf_path = f"Estructura PDF/{app['pdf']}"
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    st.download_button(label="📂 Manual", data=f, file_name=app['pdf'], mime="application/pdf", key=f"{key_prefix}_dl_{idx}")
            else:
                st.button("📄 Sin Manual", disabled=True, key=f"{key_prefix}_none_{idx}")

            st.link_button("Abrir Aplicación", app['url'], use_container_width=True)

    for arr_idx in arrows:
        with cols[arr_idx]:
            st.markdown('<div class="flow-arrow">➔</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


st.title("🚀 Panel Central de Aplicaciones Turaco")

st.markdown("""
<div class="intro-box">
    <p style="margin:0; font-size:0.9rem; color:white;">Hub de herramientas para la gestión de Marketplaces. Usa el <b>Índice</b> para navegación rápida o descarga los <b>Manuales</b> de estructura.</p>
</div>
""", unsafe_allow_html=True)

# --- BOTÓN DIRECTO: TAREA DIARIA CRÍTICA ---
p_col1, p_col2 = st.columns([3, 1])
with p_col1:
    st.markdown("""
    <div class="top-priority-container">
        <span style="font-size: 1.3rem; margin-right: 12px;">⚠️</span>
        <div>
            <b style="color: #3EB1C8; font-size: 1.05rem;">Tarea Diaria Prioritaria: Control Desactivados</b><br>
            <span style="color: #aaa; font-size: 0.85rem;">Acceso inmediato para la auditoría y control de activación de stock deshabilitado en catálogos.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
with p_col2:
    st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True) 
    st.link_button("🔍 Control Desactivados", "https://controldesactivados.streamlit.app/", use_container_width=True)

st.markdown('<div style="margin-top: 15px;"></div>', unsafe_allow_html=True)

search_query = st.text_input("🔍 Buscar aplicación...", "").lower()

# --- ÍNDICE RÁPIDO (justo debajo del buscador) ---
todas_las_apps = sorted(
    apps + flujo_apps + flujo2_apps + flujo3_apps + flujo4_apps + flujo5_apps + flujo6_apps + flujo7_apps + flujo8_apps,
    key=lambda k: k['nombre'].replace("❶ ", "").replace("❷ ", "").replace("❸ ", "").replace("❹ ", "")
)

if not search_query:
    with st.expander("📊 Índice rápido de acceso directo", expanded=False):
        df_index = pd.DataFrame([{"Aplicación": f'<a href="{a["url"]}" target="_blank">{a["nombre"]}</a>', "Categoría": a.get('cat', 'Flujo'), "Función": a['desc']} for a in todas_las_apps])
        st.write(df_index.to_html(escape=False, index=False), unsafe_allow_html=True)

# --- BLOQUES VISUALES DE FLUJOS SECUENCIALES (Solo si no se busca) ---
if not search_query:
    for titulo, flujo_list, key_prefix in TODOS_LOS_FLUJOS:
        render_flujo(titulo, flujo_list, key_prefix)

# --- FILTRADO Y MESH GENERAL ---
apps_filtradas = [app for app in apps if search_query in app["nombre"].lower() or search_query in app["desc"].lower() or search_query in app["cat"].lower()]

resultados_totales = list(apps_filtradas)
if search_query:
    for _, flujo_list, _ in TODOS_LOS_FLUJOS:
        resultados_totales += [app for app in flujo_list if search_query in app["nombre"].lower() or search_query in app["desc"].lower()]

st.markdown("---")

# Renderizado correcto en bloques de la parrilla general
if resultados_totales:
    cols = st.columns(4)
    for i, app in enumerate(resultados_totales):
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
            
            pdf_path = f"Estructura PDF/{app['pdf']}"
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    st.download_button(label="📂 Manual", data=f, file_name=app['pdf'], mime="application/pdf", key=f"dl_{i}")
            else:
                st.button("📄 Sin Manual", disabled=True, key=f"none_{i}")

            if app.get("has_step_prior"):
                c1, c2 = st.columns(2)
                with c1: st.link_button("❶ Conv", app['prior_url'], use_container_width=True)
                with c2: st.link_button("❷ Stock", app['url'], use_container_width=True)
            else:
                st.link_button("Abrir Aplicación", app['url'], use_container_width=True)
else:
    st.warning("No se encontraron coincidencias.")
