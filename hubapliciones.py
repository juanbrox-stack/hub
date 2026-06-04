import streamlit as st
import base64
import pandas as pd
import os

# Configuración de página
st.set_page_config(page_title="Hub de Aplicaciones · Cecotec Marketplaces", layout="wide", page_icon="⚙️")

def get_svg_base64(svg_path):
    try:
        with open(svg_path, "r") as f:
            svg = f.read()
            return base64.b64encode(svg.encode('utf-8')).decode('utf-8')
    except:
        return None

# ─────────────────────────────────────────────────────────────────────────────
# DATOS: FLUJO SECUENCIAL (NO MODIFICAR)
# ─────────────────────────────────────────────────────────────────────────────
flujo_apps = [
    {"nombre": "❶ Volcar Pedidos Cecotec", "url": "https://volcarpedidos.streamlit.app/", "icon": "marketplaces.svg", "desc": "Automatización para el volcado masivo e integración de pedidos.", "pdf": "Manual_Usuario_Volcar_Pedidos_Cecotec.pdf"},
    {"nombre": "❷ Buscar Sustituto",        "url": "https://buscarsustituto.streamlit.app/",      "icon": "marketplaces.svg", "desc": "Localización y asignación de referencias alternativas de stock.", "pdf": "Buscar_Sustituto.pdf"},
    {"nombre": "❸ Borradores Cecopartners", "url": "https://borradorescecopartners.streamlit.app/","icon": "marketplaces.svg", "desc": "Generación final y carga de borradores en la plataforma Cecopartners.", "pdf": "Borradores_Cecopartners.pdf"},
]

# ─────────────────────────────────────────────────────────────────────────────
# DATOS: GRUPOS FUNCIONALES
# Orden lógico de trabajo: Catálogo → Tarifas → Stock/Logística → Pedidos →
#   Errores → Auditoría → BI/Reporting → Facturación → Marketing → Utilidades
# ─────────────────────────────────────────────────────────────────────────────
grupos = [
    {
        "id": "catalogo",
        "titulo": "📦 Catálogo y Contenido",
        "desc": "Creación, enriquecimiento y publicación de fichas de producto.",
        "apps": [
            {"nombre": "Amazon Bulk Master",                          "url": "https://rellenaplantillasamazon.streamlit.app/",      "icon": "stockamazon.svg",     "desc": "Rellena plantillas de Amazon de forma masiva y automatizada.",                  "pdf": "Manual_Amazon_Bulk_Master_v101_es-ES.pdf"},
            {"nombre": "Actualiza URLs de Imágenes",                  "url": "https://actualizaurlsimagenes.streamlit.app/",        "icon": "marketplaces.svg",    "desc": "Edición masiva de rutas de imágenes en ficheros.",                              "pdf": "Actualiza URLs.pdf"},
            {"nombre": "Concatenar URLs PIM para PrestaShop",         "url": "https://concatenarurl.streamlit.app/",               "icon": "marketplaces.svg",    "desc": "Generador de URLs absolutas para imágenes de productos.",                       "pdf": "Extractor de URLs para PrestaShop.pdf"},
            {"nombre": "Características PS 2026",                     "url": "https://caracteristicaspsturaco2026.streamlit.app/",  "icon": "featuresps.svg",      "desc": "Gestión avanzada de características PrestaShop 2026.",                          "pdf": "Características 2026.pdf"},
            {"nombre": "Crea Ficheros de Características Herramientas","url": "https://featuresps.streamlit.app",                   "icon": "featuresps.svg",      "desc": "Creación del fichero de características para herramientas.",                   "pdf": "Features PS.pdf"},
            {"nombre": "Creación de Novedades PrestaShop (PS Bridge)", "url": "https://ps-bridge.streamlit.app",                   "icon": "ps-bridge.svg",       "desc": "Fichero de subida de novedades a PrestaShop.",                                  "pdf": "PS Bridge.pdf"},
            {"nombre": "Unidad Nueva",                                 "url": "https://unidadnueva.streamlit.app",                  "icon": "unidadnueva.svg",     "desc": "Subida a Cecopartners de pedidos automatizada.",                                "pdf": "Unidad Nueva.pdf"},
            {"nombre": "Variaciones Cdiscount",                        "url": "https://variacionescdiscount.streamlit.app/",        "icon": "marketplaces.svg",    "desc": "Generador de variaciones específicas para Cdiscount.",                          "pdf": "Variaciones Cdiscount.pdf"},
            {"nombre": "Explorador Categorías y Campos MediaMarkt",    "url": "https://atributosmediamarkt.streamlit.app/",         "icon": "marketplaces.svg",    "desc": "Explorador de categorías y atributos específicos para MediaMarkt.",            "pdf": "Manual_MM_Category_Explorer.pdf"},
            {"nombre": "Recortador de Títulos y Descripciones",        "url": "https://recortadorcadenastexto.streamlit.app/",      "icon": "marketplaces.svg",    "desc": "Limpieza y recorte de longitud de textos para marketplaces.",                  "pdf": "Recortador Cadenas.pdf"},
        ],
    },
    {
        "id": "tarifas",
        "titulo": "💶 Tarifas y Precios",
        "desc": "Generación, actualización y carga de ficheros de tarificación.",
        "apps": [
            {"nombre": "Actualizador de Tarifas",                      "url": "https://actualizardortarifas.streamlit.app",           "icon": "actualizardortarifas.svg", "desc": "Gestión y actualización de tarifas; genera el fichero completo.",              "pdf": "Actualizador Tarifas.pdf"},
            {"nombre": "Actualizador Tarifas Herramientas",             "url": "https://creaficherostarifasherramientas.streamlit.app/","icon": "actualizardortarifas.svg", "desc": "Generador y actualizador automatizado de ficheros de tarifas de herramientas.","pdf": "Manual_de_Usuario_Actualizador_Tarifas.pdf"},
            {"nombre": "Generador Plantilla Tarifas Amazon",            "url": "https://generarplantillatarifasamazon.streamlit.app/", "icon": "stockamazon.svg",          "desc": "Generación de plantillas de tarifas personalizadas para Amazon.",              "pdf": "Manual_Generador_Tarifas_Amazon.pdf"},
        ],
    },
    {
        "id": "stock_logistica",
        "titulo": "🚚 Stock y Logística",
        "desc": "Control de inventario, envíos y mapeo de categorías.",
        "apps": [
            {"nombre": "Stock Amazon",            "url": "https://stockamazon.streamlit.app",           "icon": "stockamazon.svg",  "desc": "Gestión de stock en Amazon (convertir antes a .xlsx si es necesario).", "pdf": "Stock Amazon.pdf", "has_step_prior": True, "prior_url": "https://convertirexcels.streamlit.app/"},
            {"nombre": "Seguimientos Amazon",     "url": "https://seguimientosamazon.streamlit.app/",   "icon": "stockamazon.svg",  "desc": "Seguimiento y control de pedidos en Amazon.",                          "pdf": "Seguimientos Amazon.pdf"},
            {"nombre": "SellerFlex FR",           "url": "https://sellerflexfr.streamlit.app/",          "icon": "marketplaces.svg", "desc": "Gestión y optimización de envíos SellerFlex para el almacén de Francia.", "pdf": "Manual_Usuario_SellerFlex_FR.pdf"},
            {"nombre": "Mapear Categorías PS vs Amazon", "url": "https://mapcategories.streamlit.app",  "icon": "mapcategories.svg","desc": "Mapeo lógico de categorías Amazon vs PrestaShop.",                      "pdf": "Map Categories.pdf"},
        ],
    },
    {
        "id": "scraping",
        "titulo": "⬇️ Descarga y Scraping de Datos",
        "desc": "Extracción masiva de datos desde webs, PIM y catálogos.",
        "apps": [
            {"nombre": "Cecotec Descarga Feed Países",    "url": "https://cecotec-downloader.streamlit.app",  "icon": "cecotec-downloader.svg", "desc": "Descarga de catálogos y datos de la web de Cecotec.",                     "pdf": "Cecotec Downloader.pdf"},
            {"nombre": "Descarga Masiva Banco de Imágenes y PIM", "url": "https://descargaspim.streamlit.app/","icon": "marketplaces.svg",    "desc": "Descarga masiva de activos y datos desde el PIM Plytix.",                "pdf": "manual_plytix_downloader.pdf"},
        ],
    },
    {
        "id": "errores",
        "titulo": "🔧 Gestión de Errores",
        "desc": "Diagnóstico y resolución de errores de publicación en marketplaces.",
        "apps": [
            {"nombre": "Errores BeezUP", "url": "https://erroresbeezup.streamlit.app/",  "icon": "marketplaces.svg", "desc": "Gestor de errores de publicación específicos de BeezUP.",          "pdf": "Errores BeezUP.pdf"},
            {"nombre": "Errores Mirakl", "url": "https://errors.streamlit.app/",          "icon": "marketplaces.svg", "desc": "Analizador de errores de publicación Mirakl / Marketplaces.",       "pdf": "Errors.pdf"},
            {"nombre": "Revisar URLs de Fotos", "url": "https://revisarurlimagenes.streamlit.app/", "icon": "marketplaces.svg", "desc": "Validación masiva de URLs de imágenes para evitar errores 404.", "pdf": "Revisar URL Fotos.pdf"},
        ],
    },
    {
        "id": "auditoria",
        "titulo": "🔍 Auditoría de Catálogo",
        "desc": "Comparativas y detección de discrepancias entre sistemas y canales.",
        "apps": [
            {"nombre": "SKUs Faltantes Amazon",  "url": "https://skusfaltantesamazon.streamlit.app/",   "icon": "stockamazon.svg",  "desc": "Auditoría y comparativa para la detección de SKUs faltantes en Amazon.", "pdf": "ManualCompartivaProductosCreadosAmazonJabiruTuraco.pdf"},
            {"nombre": "Comparador Bestseller",  "url": "https://comparadorbestseller.streamlit.app/",  "icon": "marketplaces.svg", "desc": "Herramienta de comparación y auditoría para productos Bestseller.",       "pdf": "Manual_Usuario_Comparador_Bestseller_v3.pdf"},
            {"nombre": "Comparar PS vs Amazon",  "url": "https://compararpsvsamazon.streamlit.app/",    "icon": "marketplaces.svg", "desc": "Auditoría de catálogo PrestaShop vs Amazon.",                           "pdf": "Comparar PS vs Amazon.pdf"},
        ],
    },
    {
        "id": "bi",
        "titulo": "📊 Business Intelligence y Reporting",
        "desc": "Análisis de ventas, rendimiento y métricas de marketplaces.",
        "apps": [
            {"nombre": "Analiza Ventas por Marketplaces", "url": "https://multitienda-bi-group.streamlit.app",   "icon": "marketplaces.svg", "desc": "BI de pedidos y análisis de ventas por marketplace y año.",              "pdf": "Marketplaces.pdf"},
            {"nombre": "InformeSeller",                   "url": "https://informeseller.streamlit.app/",          "icon": "marketplaces.svg", "desc": "Generación de informes detallados de ventas y rendimiento Seller.",       "pdf": "InformeSeller.pdf"},
            {"nombre": "Informe Ventas Marketing",        "url": "https://automatizacionventasmkt.streamlit.app/","icon": "marketplaces.svg", "desc": "Análisis estratégico y automatización de informes para Marketing.",       "pdf": "Manual_Usuario_Informe_Ventas_MKT.pdf"},
            {"nombre": "Reviews Tracker",                 "url": "https://reviewstracker.streamlit.app",           "icon": "marketplaces.svg", "desc": "Seguimiento y análisis de reseñas de clientes.",                         "pdf": "Reviews Tracker.pdf"},
        ],
    },
    {
        "id": "facturacion",
        "titulo": "🧾 Facturación y Comisiones",
        "desc": "Transformación de ficheros de facturación y cálculo de comisiones.",
        "apps": [
            {"nombre": "Amazon Facturas",       "url": "https://transformarexcelamazonfacturas.streamlit.app/", "icon": "stockamazon.svg",  "desc": "Transformación de ficheros para facturación Amazon.",                      "pdf": "Amazon Facturas.pdf"},
            {"nombre": "Comisiones MediaMarkt", "url": "https://comisionesmediamarkt.streamlit.app/",           "icon": "marketplaces.svg", "desc": "Cálculo y desglose de comisiones para el marketplace de MediaMarkt.",     "pdf": "Manual_Comisiones_MediaMarkt_v12.pdf"},
        ],
    },
    {
        "id": "utilidades",
        "titulo": "🛠️ Utilidades Generales",
        "desc": "Herramientas transversales de productividad y análisis de rentabilidad.",
        "apps": [
            {"nombre": "Dividir Excel",                 "url": "https://dividirexcel.streamlit.app/",                  "icon": "marketplaces.svg", "desc": "Separa archivos Excel en múltiples pestañas o ficheros.",                "pdf": "Dividir Excel.pdf"},
            {"nombre": "Calculadora ROI Automatización","url": "https://calculadoraretornoinversion.streamlit.app/",   "icon": "marketplaces.svg", "desc": "Calcula el ahorro y rentabilidad de proyectos de automatización.",       "pdf": "Calculadora_ROI_Automatizacion.pdf"},
            {"nombre": "Tipo Dispositivo",              "url": "https://tipodispositivo.streamlit.app/",               "icon": "marketplaces.svg", "desc": "Identificación del tipo de dispositivo de acceso.",                     "pdf": "Tipo Dispositivo.pdf"},
        ],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# LISTA PLANA (para índice y búsqueda)
# ─────────────────────────────────────────────────────────────────────────────
todas_apps_generales = []
for g in grupos:
    for a in g["apps"]:
        todas_apps_generales.append({**a, "cat": g["titulo"]})

todas_las_apps = sorted(
    todas_apps_generales + flujo_apps,
    key=lambda k: k["nombre"].replace("❶ ", "").replace("❷ ", "").replace("❸ ", "")
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}

.stApp {
    background-color: #141413;
    color: #FAF9F5;
}

/* ── Inputs y labels ── */
[data-testid="stTextInput"] label p { color: #FAF9F5 !important; font-weight: 700; }
[data-testid="stTextInput"] input {
    color: #FAF9F5 !important;
    background-color: #1e1e1d !important;
    border: 1px solid #3EB1C8 !important;
    border-radius: 8px !important;
}

/* ── Expander índice ── */
.stExpander { background-color: #1e1e1d !important; border: 1px solid #2a2a29 !important; border-radius: 10px !important; }
.stExpander [data-testid="stHeader"] p { color: #FAF9F5 !important; font-weight: 700; }
.stExpander [data-testid="stExpanderDetails"] { background-color: #1e1e1d !important; }
table { background-color: #1e1e1d !important; color: #FAF9F5 !important; width: 100%; }
th { color: #3EB1C8 !important; border-bottom: 1px solid #3EB1C8 !important; padding: 8px 12px !important; }
td { padding: 6px 12px !important; border-bottom: 1px solid #2a2a29 !important; }

/* ── Header ── */
.hub-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 6px;
}
.hub-title {
    font-size: 2rem;
    font-weight: 800;
    color: #FAF9F5;
    margin: 0;
    line-height: 1;
}
.hub-title span { color: #3EB1C8; }
.hub-sub {
    font-size: 0.9rem;
    color: #888;
    margin: 4px 0 0 0;
}

/* ── Intro box ── */
.intro-box {
    background-color: #1a1a19;
    padding: 11px 16px;
    border-radius: 10px;
    border-left: 4px solid #3EB1C8;
    margin-bottom: 18px;
    font-size: 0.88rem;
    color: #c8c8c4;
}
.intro-box b { color: #3EB1C8; }

/* ── Divisor de grupo ── */
.group-header {
    display: flex;
    align-items: baseline;
    gap: 12px;
    margin: 28px 0 4px 0;
    padding-bottom: 8px;
    border-bottom: 2px solid #3EB1C8;
}
.group-title {
    font-size: 1.15rem;
    font-weight: 800;
    color: #FAF9F5;
    margin: 0;
}
.group-desc {
    font-size: 0.82rem;
    color: #888;
    margin: 0;
}

/* ── Tarjeta de app ── */
.app-card {
    background-color: #FAF9F5;
    border-radius: 12px;
    border: 1px solid #ddd;
    padding: 14px 14px 10px 14px;
    min-height: 138px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    text-align: center;
    margin-bottom: 10px;
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}
.app-card:hover {
    box-shadow: 0 4px 18px rgba(62,177,200,0.22);
    transform: translateY(-2px);
}
.card-title {
    color: #141413 !important;
    margin: 6px 0 0 0;
    font-size: 1rem;
    font-weight: 800;
    line-height: 1.2;
}
.card-desc {
    color: #444 !important;
    font-size: 0.8rem;
    margin-top: 5px;
    line-height: 1.3;
    font-weight: 500;
}

/* ── Flujo secuencial ── */
.workflow-container {
    background-color: #1a1a19;
    padding: 20px 22px;
    border-radius: 15px;
    border: 2px dashed #3EB1C8;
    margin: 22px 0 10px 0;
}
.workflow-title {
    color: #3EB1C8 !important;
    font-size: 1.1rem;
    font-weight: 800;
    margin-bottom: 14px;
    text-align: left;
}
.flow-arrow {
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 2rem;
    color: #3EB1C8;
    height: 138px;
}

/* ── Botones ── */
div.stButton > button,
div.stDownloadButton > button,
div.stLinkButton > a {
    background-color: #3EB1C8 !important;
    color: #141413 !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 0.78rem !important;
    height: 2.8em !important;
    width: 100% !important;
    margin: 4px 0 !important;
    border: none !important;
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    text-decoration: none !important;
    transition: background-color 0.2s ease, color 0.2s ease;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover,
div.stLinkButton > a:hover {
    background-color: #FAF9F5 !important;
    color: #141413 !important;
}

div.stButton > button:disabled {
    background-color: #2a2a29 !important;
    color: #666 !important;
    cursor: not-allowed;
}

a { color: #3EB1C8 !important; text-decoration: none; font-weight: bold; }

/* ── Badge de categoría ── */
.cat-badge {
    display: inline-block;
    background-color: #1e1e1d;
    color: #3EB1C8;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 20px;
    margin-bottom: 4px;
    border: 1px solid #3EB1C8;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hub-header">
    <div>
        <p class="hub-title">⚙️ Hub de <span>Aplicaciones</span></p>
        <p class="hub-sub">Cecotec Marketplaces &amp; Content Online · Desarrollado por Juan Brox</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="intro-box">
    Herramientas integradas para la gestión de Marketplaces. Usa el <b>Índice rápido</b> para navegación directa
    o explora los grupos por funcionalidad. Descarga los <b>Manuales PDF</b> desde cada tarjeta.
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# BUSCADOR
# ─────────────────────────────────────────────────────────────────────────────
search_query = st.text_input("🔍 Buscar aplicación...", "").strip().lower()

# ─────────────────────────────────────────────────────────────────────────────
# BLOQUE FLUJO SECUENCIAL (NO MODIFICAR)
# ─────────────────────────────────────────────────────────────────────────────
if not search_query:
    st.markdown('<div class="workflow-container"><div class="workflow-title">🔄 Flujo de Trabajo Secuencial: Gestión de Pedidos Cecotec</div>', unsafe_allow_html=True)

    f_cols = st.columns([3, 0.5, 3, 0.5, 3])
    indices_flujo = [0, 2, 4]
    arrows_flujo  = [1, 3]

    for idx, app in enumerate(flujo_apps):
        with f_cols[indices_flujo[idx]]:
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
                    st.download_button(label="📂 Manual", data=f, file_name=app['pdf'], mime="application/pdf", key=f"flow_dl_{idx}")
            else:
                st.button("📄 Sin Manual", disabled=True, key=f"flow_none_{idx}")

            st.link_button("Abrir Aplicación", app['url'], use_container_width=True)

    for arr_idx in arrows_flujo:
        with f_cols[arr_idx]:
            st.markdown('<div class="flow-arrow">➔</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ÍNDICE RÁPIDO (solo sin búsqueda activa)
# ─────────────────────────────────────────────────────────────────────────────
if not search_query:
    with st.expander("📋 Índice rápido de acceso directo", expanded=False):
        df_index = pd.DataFrame([
            {
                "Aplicación": f'<a href="{a["url"]}" target="_blank">{a["nombre"]}</a>',
                "Grupo": a.get("cat", "Flujo Cecotec"),
                "Función": a["desc"]
            }
            for a in todas_las_apps
        ])
        st.write(df_index.to_html(escape=False, index=False), unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HELPER: renderizar tarjeta + botones
# ─────────────────────────────────────────────────────────────────────────────
def render_card(app, key_suffix):
    b64_icon = get_svg_base64(f"iconos/{app['icon']}")
    icon_html = f'<img src="data:image/svg+xml;base64,{b64_icon}" width="32" style="margin-bottom:4px;"/>' if b64_icon else "📦"

    st.markdown(f"""
        <div class="app-card">
            {icon_html}
            <div class="card-title">{app['nombre']}</div>
            <div class="card-desc">{app['desc']}</div>
        </div>
    """, unsafe_allow_html=True)

    pdf_path = f"Estructura PDF/{app['pdf']}"
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            st.download_button(label="📂 Manual", data=f, file_name=app['pdf'], mime="application/pdf", key=f"dl_{key_suffix}")
    else:
        st.button("📄 Sin Manual", disabled=True, key=f"none_{key_suffix}")

    if app.get("has_step_prior"):
        c1, c2 = st.columns(2)
        with c1:
            st.link_button("❶ Convertir", app['prior_url'], use_container_width=True)
        with c2:
            st.link_button("❷ Stock", app['url'], use_container_width=True)
    else:
        st.link_button("Abrir Aplicación", app['url'], use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# MODO BÚSQUEDA
# ─────────────────────────────────────────────────────────────────────────────
if search_query:
    resultados = [
        a for a in todas_las_apps
        if search_query in a["nombre"].lower()
        or search_query in a["desc"].lower()
        or search_query in a.get("cat", "").lower()
    ]

    if resultados:
        st.markdown(f"<p style='color:#888; font-size:0.85rem; margin:8px 0 16px 0;'>{len(resultados)} resultado(s) para <b style='color:#3EB1C8;'>«{search_query}»</b></p>", unsafe_allow_html=True)
        cols = st.columns(4)
        for i, app in enumerate(resultados):
            with cols[i % 4]:
                render_card(app, f"search_{i}")
    else:
        st.warning("No se encontraron coincidencias.")

# ─────────────────────────────────────────────────────────────────────────────
# MODO NORMAL: grupos funcionales
# ─────────────────────────────────────────────────────────────────────────────
else:
    for grupo in grupos:
        st.markdown(f"""
        <div class="group-header">
            <p class="group-title">{grupo['titulo']}</p>
            <p class="group-desc">{grupo['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

        apps_grupo = grupo["apps"]
        cols = st.columns(4)
        for i, app in enumerate(apps_grupo):
            with cols[i % 4]:
                render_card(app, f"{grupo['id']}_{i}")

    st.markdown("<br>", unsafe_allow_html=True)
