import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_dataframe
from visualizations import (
    visualize_datos_generales,
    visualize_rebano,
    visualize_energia,
    visualize_superficies
)

def show_dashboard():
    """Display the general dashboard with data visualizations"""
    st.title("Dashboard General")
    
    # Check if we have any data
    datos_df = load_dataframe("datos_generales.csv")
    rebano_df = load_dataframe("rebano.csv")
    energia_df = load_dataframe("energia.csv")
    superficies_df = load_dataframe("superficies_insumos.csv")
    
    # Check if there's enough data to display visualizations
    has_basic_data = not datos_df.empty or not rebano_df.empty
    
    if not has_basic_data:
        st.warning("⚠️ No hay suficientes datos para generar visualizaciones. Por favor complete al menos las secciones 'Datos Generales' y 'Rebaño'.")
        return
    
    # Show farm information if available
    if not datos_df.empty and 'nombre_tambo' in datos_df.columns:
        farm_name = datos_df['nombre_tambo'].iloc[-1]
        st.subheader(f"Visualizaciones para: {farm_name}")
    
    # Create tabbed interface for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["Datos Generales", "Rebaño", "Energía", "Superficies"])
    
    with tab1:
        if not datos_df.empty:
            visualize_datos_generales()
        else:
            st.warning("No hay datos en la sección Datos Generales para visualizar.")
    
    with tab2:
        if not rebano_df.empty:
            visualize_rebano()
        else:
            st.warning("No hay datos en la sección Rebaño para visualizar.")
    
    with tab3:
        if not energia_df.empty:
            visualize_energia()
        else:
            st.warning("No hay datos en la sección Energía para visualizar.")
    
    with tab4:
        if not superficies_df.empty:
            visualize_superficies()
        else:
            st.warning("No hay datos en la sección Superficies e Insumos para visualizar.")
    
    # Data completeness indicator
    st.subheader("Completitud de Datos")
    
    # Define all sections
    sections = [
        "Datos Generales",
        "Superficies e Insumos",
        "Manejo y Recursos",
        "Fertilización",
        "Protección de Cultivos",
        "Riego / Uso de Agua",
        "Energía",
        "Rebaño",
        "Gestión de Efluentes",
        "Transporte"
    ]
    
    # Check which sections have data
    section_files = {
        "Datos Generales": "datos_generales.csv",
        "Superficies e Insumos": "superficies_insumos.csv",
        "Manejo y Recursos": "manejo.csv",
        "Fertilización": "fertilizacion.csv",
        "Protección de Cultivos": "proteccion_cultivos.csv",
        "Riego / Uso de Agua": "riego.csv",
        "Energía": "energia.csv",
        "Rebaño": "rebano.csv",
        "Gestión de Efluentes": "efluentes.csv",
        "Transporte": "transporte.csv"
    }
    
    section_data = []
    for section, file in section_files.items():
        df = load_dataframe(file)
        has_data = not df.empty
        section_data.append({"Sección": section, "Completado": 100 if has_data else 0})
    
    completeness_df = pd.DataFrame(section_data)
    
    # Create a horizontal bar chart for data completeness
    fig = px.bar(
        completeness_df,
        x="Completado",
        y="Sección",
        orientation='h',
        title="Completitud de Datos por Sección",
        labels={"Completado": "Porcentaje Completado", "Sección": ""},
        color="Completado",
        color_continuous_scale=["#fa4343", "#fae043", "#43fa9c"],
        range_color=[0, 100]
    )
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        title_font=dict(size=18),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Calculate overall completeness
    completed_sections = sum(1 for section in section_data if section["Completado"] > 0)
    overall_completeness = (completed_sections / len(sections)) * 100
    
    st.metric("Completitud General", f"{overall_completeness:.0f}%")
