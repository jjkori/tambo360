import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import load_dataframe
from visualizations import create_pie_chart, create_bar_chart, create_scatter_plot

def show_resumen_rebano():
    """Display a detailed summary of the cattle herd"""
    st.title("Resumen del Rebaño")
    
    # Load rebaño data
    df = load_dataframe("rebano.csv")
    
    if df.empty:
        st.warning("⚠️ No hay datos de rebaño para visualizar. Por favor complete primero la sección 'Rebaño'.")
        return
    
    # Summary metrics
    st.subheader("Métricas Principales")
    
    # Total animals and categories
    total_animals = df['número_animales'].sum() if 'número_animales' in df.columns else 0
    num_categories = df['categoría'].nunique() if 'categoría' in df.columns else 0
    
    # Calculate total weight and consumption
    if all(col in df.columns for col in ['número_animales', 'peso_promedio']):
        total_weight = sum(df['número_animales'] * df['peso_promedio'])
    else:
        total_weight = 0
    
    if all(col in df.columns for col in ['número_animales', 'dieta_materia_seca']):
        total_dry_matter = sum(df['número_animales'] * df['dieta_materia_seca'])
    else:
        total_dry_matter = 0
    
    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Animales", f"{total_animals}")
    
    with col2:
        st.metric("Categorías", f"{num_categories}")
    
    with col3:
        st.metric("Peso Total", f"{total_weight:.0f} kg")
    
    with col4:
        st.metric("Consumo MS Total", f"{total_dry_matter:.0f} kg/día")
    
    # Create visualizations
    st.subheader("Distribución del Rebaño")
    
    # Distribution by category
    if 'categoría' in df.columns and 'número_animales' in df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart of animal distribution
            fig_distribution = create_pie_chart(
                df, 
                'categoría', 
                'número_animales', 
                'Distribución por Categoría'
            )
            st.plotly_chart(fig_distribution, use_container_width=True)
        
        with col2:
            # Bar chart of animals per category
            fig_animals = create_bar_chart(
                df, 
                'categoría', 
                'número_animales', 
                'Animales por Categoría',
                orientation='h'
            )
            st.plotly_chart(fig_animals, use_container_width=True)
    
    # Weight and consumption analysis
    st.subheader("Análisis de Peso y Consumo")
    
    if all(col in df.columns for col in ['categoría', 'peso_promedio', 'número_animales']):
        # Create weight data
        weight_data = df.copy()
        weight_data['peso_total'] = weight_data['número_animales'] * weight_data['peso_promedio']
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Bar chart of average weight by category
            fig_weight = create_bar_chart(
                df,
                'categoría',
                'peso_promedio',
                'Peso Promedio por Categoría (kg)'
            )
            st.plotly_chart(fig_weight, use_container_width=True)
        
        with col2:
            # Pie chart of total weight distribution
            fig_total_weight = create_pie_chart(
                weight_data,
                'categoría',
                'peso_total',
                'Distribución del Peso Total'
            )
            st.plotly_chart(fig_total_weight, use_container_width=True)
    
    # Grazing and feeding patterns
    if all(col in df.columns for col in ['categoría', 'horas_pastoreo', 'dieta_materia_seca', 'número_animales']):
        st.subheader("Patrones de Pastoreo y Alimentación")
        
        # Scatter plot of grazing hours vs dry matter intake
        fig_grazing = create_scatter_plot(
            df,
            'horas_pastoreo',
            'dieta_materia_seca',
            'Relación entre Horas de Pastoreo y Consumo de Materia Seca',
            size='número_animales',
            color='categoría'
        )
        st.plotly_chart(fig_grazing, use_container_width=True)
    
    # Diet composition if available
    diet_columns = ['porcentaje_pastura', 'porcentaje_concentrado', 'porcentaje_otros']
    if all(col in df.columns for col in diet_columns):
        st.subheader("Composición de la Dieta")
        
        # Calculate weighted average diet composition based on animal numbers
        diet_data = {
            'Componente': ['Pastura', 'Concentrado', 'Otros'],
            'Porcentaje': [
                sum(df['porcentaje_pastura'] * df['número_animales']) / total_animals,
                sum(df['porcentaje_concentrado'] * df['número_animales']) / total_animals,
                sum(df['porcentaje_otros'] * df['número_animales']) / total_animals
            ]
        }
        
        diet_df = pd.DataFrame(diet_data)
        
        # Pie chart of diet composition
        fig_diet = create_pie_chart(
            diet_df,
            'Componente',
            'Porcentaje',
            'Composición Promedio de la Dieta'
        )
        st.plotly_chart(fig_diet, use_container_width=True)
    
    # Detailed table with all data
    st.subheader("Datos Detallados del Rebaño")
    display_df = df.drop(columns=['uuid']) if 'uuid' in df.columns else df
    st.dataframe(display_df)
