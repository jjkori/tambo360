import streamlit as st
import os
import pandas as pd
from streamlit_option_menu import option_menu

# Import sections
from sections.home import show_home
from sections.datos_generales import show_datos_generales
from sections.superficies_insumos import show_superficies_insumos
from sections.manejo_recursos import show_manejo_recursos
from sections.fertilizacion import show_fertilizacion
from sections.proteccion_cultivos import show_proteccion_cultivos
from sections.riego import show_riego
from sections.energia import show_energia
from sections.rebano import show_rebano
from sections.efluentes import show_efluentes
from sections.transporte import show_transporte
from sections.dashboard import show_dashboard
from sections.resumen_rebano import show_resumen_rebano

# Import export functions
from exporters import export_to_word, export_to_excel

# Ensure data directory exists
if not os.path.exists("data"):
    os.makedirs("data")

# Page config
st.set_page_config(
    page_title="FieldLens - Recolección de Datos en Tambos",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state variables if not exist
if "current_section" not in st.session_state:
    st.session_state.current_section = "Inicio"

if "farm_name" not in st.session_state:
    st.session_state.farm_name = ""

# Sidebar with navigation
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>FieldLens</h1>", unsafe_allow_html=True)
    
    # Display logo
    st.markdown("""
    <div style='text-align: center;'>
        <svg width="100" height="100" viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="40" stroke="#4380fa" stroke-width="3" fill="none" />
            <path d="M30,50 L45,65 L70,35" stroke="#4380fa" stroke-width="3" fill="none" />
        </svg>
    </div>
    """, unsafe_allow_html=True)
    
    # Main menu
    menu_selection = option_menu(
        "Menú Principal",
        [
            "🏡 Inicio",
            "📋 Datos Generales",
            "🌱 Superficies e Insumos",
            "🛠️ Manejo y Recursos",
            "🌿 Fertilización",
            "🔒 Protección de Cultivos",
            "💧 Riego / Uso de Agua",
            "⚡ Energía",
            "🐄 Rebaño",
            "📊 Resumen Rebaño",
            "🧪 Gestión de Efluentes",
            "🚚 Transporte",
            "📈 Dashboard General",
            "📄 Exportar Word + PDF",
            "📊 Exportar Excel",
        ],
        default_index=0,
    )
    
    st.session_state.current_section = menu_selection
    
    # Display farm name if set
    if st.session_state.farm_name:
        st.info(f"Tambo actual: {st.session_state.farm_name}")
    
    # Button to start new data collection
    if st.button("🔄 Recolectar Datos", use_container_width=True):
        # Reset session state for a new data collection
        for key in list(st.session_state.keys()):
            if key not in ["current_section"]:
                st.session_state.pop(key, None)
        st.info("¡Nueva sesión de recolección iniciada!")
    
    st.divider()
    st.caption("by Cultura CŌW | Design by La Vaca Studio")

# Display the corresponding section based on menu selection
if st.session_state.current_section == "🏡 Inicio":
    show_home()
elif st.session_state.current_section == "📋 Datos Generales":
    show_datos_generales()
elif st.session_state.current_section == "🌱 Superficies e Insumos":
    show_superficies_insumos()
elif st.session_state.current_section == "🛠️ Manejo y Recursos":
    show_manejo_recursos()
elif st.session_state.current_section == "🌿 Fertilización":
    show_fertilizacion()
elif st.session_state.current_section == "🔒 Protección de Cultivos":
    show_proteccion_cultivos()
elif st.session_state.current_section == "💧 Riego / Uso de Agua":
    show_riego()
elif st.session_state.current_section == "⚡ Energía":
    show_energia()
elif st.session_state.current_section == "🐄 Rebaño":
    show_rebano()
elif st.session_state.current_section == "📊 Resumen Rebaño":
    show_resumen_rebano()
elif st.session_state.current_section == "🧪 Gestión de Efluentes":
    show_efluentes()
elif st.session_state.current_section == "🚚 Transporte":
    show_transporte()
elif st.session_state.current_section == "📈 Dashboard General":
    show_dashboard()
elif st.session_state.current_section == "📄 Exportar Word + PDF":
    export_to_word()
elif st.session_state.current_section == "📊 Exportar Excel":
    export_to_excel()
