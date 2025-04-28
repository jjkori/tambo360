import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from utils import load_dataframe

def generate_graph_color_palette(num_colors=10):
    """Generate a color palette for graphs"""
    base_colors = ["#4380fa", "#43c6fa", "#fa4343", "#43fa9c", "#fae043", 
                   "#fa43c6", "#43faed", "#fa9c43", "#c6fa43", "#b243fa"]
    return base_colors[:num_colors]

def create_pie_chart(data, names, values, title):
    """Create a pie chart"""
    fig = px.pie(
        data, 
        names=names, 
        values=values, 
        title=title,
        color_discrete_sequence=generate_graph_color_palette()
    )
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        title_font=dict(size=18)
    )
    return fig

def create_bar_chart(data, x, y, title, orientation='v'):
    """Create a bar chart"""
    fig = px.bar(
        data, 
        x=x if orientation == 'v' else y, 
        y=y if orientation == 'v' else x, 
        title=title,
        orientation=orientation,
        color_discrete_sequence=generate_graph_color_palette()
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        title_font=dict(size=18)
    )
    return fig

def create_line_chart(data, x, y, title):
    """Create a line chart"""
    fig = px.line(
        data, 
        x=x, 
        y=y, 
        title=title,
        markers=True,
        color_discrete_sequence=generate_graph_color_palette()
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        title_font=dict(size=18)
    )
    return fig

def create_scatter_plot(data, x, y, title, size=None, color=None):
    """Create a scatter plot"""
    fig = px.scatter(
        data, 
        x=x, 
        y=y, 
        title=title,
        size=size,
        color=color,
        color_discrete_sequence=generate_graph_color_palette()
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        title_font=dict(size=18)
    )
    return fig

def create_gauge_chart(value, min_val, max_val, title, suffix=""):
    """Create a gauge chart"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title},
        gauge={
            "axis": {"range": [min_val, max_val]},
            "bar": {"color": "#4380fa"},
            "steps": [
                {"range": [min_val, max_val/3], "color": "#fa4343"},
                {"range": [max_val/3, 2*max_val/3], "color": "#fae043"},
                {"range": [2*max_val/3, max_val], "color": "#43fa9c"}
            ]
        },
        number={"suffix": suffix}
    ))
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        title_font=dict(size=18),
        height=250
    )
    return fig

def visualize_datos_generales():
    """Create visualizations for Datos Generales"""
    df = load_dataframe("datos_generales.csv")
    if df.empty:
        st.warning("No hay datos en la sección Datos Generales para visualizar.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Create pie chart for milk distribution
        if all(x in df.columns for x in ['venta_industria', 'uso_queseria', 'descarte']):
            milk_data = pd.DataFrame({
                'Destino': ['Venta Industria', 'Uso Quesería', 'Descarte'],
                'Porcentaje': [df['venta_industria'].iloc[0], df['uso_queseria'].iloc[0], df['descarte'].iloc[0]]
            })
            fig_milk = create_pie_chart(milk_data, 'Destino', 'Porcentaje', 'Distribución de la Producción de Leche')
            st.plotly_chart(fig_milk, use_container_width=True)
    
    with col2:
        # Create gauge for milk production
        if 'produccion_ind' in df.columns:
            fig_production = create_gauge_chart(
                df['produccion_ind'].iloc[0], 
                0, 
                50,  # Assuming max production is 50 liters
                "Producción Individual",
                " l/vaca/día"
            )
            st.plotly_chart(fig_production, use_container_width=True)
    
    # Land distribution
    if 'sup_total' in df.columns and 'sup_vt' in df.columns:
        sup_vt = df['sup_vt'].iloc[0]
        sup_other = df['sup_total'].iloc[0] - sup_vt
        
        land_data = pd.DataFrame({
            'Tipo': ['Vacas en Ordeñe', 'Otros Usos'],
            'Hectáreas': [sup_vt, sup_other if sup_other > 0 else 0]
        })
        
        fig_land = create_bar_chart(land_data, 'Tipo', 'Hectáreas', 'Distribución de Superficie')
        st.plotly_chart(fig_land, use_container_width=True)

def visualize_rebano():
    """Create visualizations for Rebano"""
    df = load_dataframe("rebano.csv")
    if df.empty:
        st.warning("No hay datos en la sección Rebaño para visualizar.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Animal distribution by category
        if 'categoría' in df.columns and 'número_animales' in df.columns:
            fig_animals = create_pie_chart(
                df, 
                'categoría', 
                'número_animales', 
                'Distribución de Animales por Categoría'
            )
            st.plotly_chart(fig_animals, use_container_width=True)
    
    with col2:
        # Weight distribution
        if 'categoría' in df.columns and 'peso_promedio' in df.columns:
            fig_weight = create_bar_chart(
                df, 
                'categoría', 
                'peso_promedio', 
                'Peso Promedio por Categoría (kg)',
                orientation='h'
            )
            st.plotly_chart(fig_weight, use_container_width=True)
    
    # Diet and grazing visualization
    if all(x in df.columns for x in ['categoría', 'horas_pastoreo', 'dieta_materia_seca']):
        st.subheader("Pastoreo y Alimentación")
        fig_grazing = px.scatter(
            df,
            x='horas_pastoreo',
            y='dieta_materia_seca',
            size='número_animales',
            color='categoría',
            hover_name='categoría',
            title='Relación entre Horas de Pastoreo y Consumo de Materia Seca',
            labels={
                'horas_pastoreo': 'Horas de Pastoreo (h/día)',
                'dieta_materia_seca': 'Consumo de Materia Seca (kg MS/animal/día)',
                'número_animales': 'Número de Animales'
            },
            color_discrete_sequence=generate_graph_color_palette()
        )
        fig_grazing.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            title_font=dict(size=18)
        )
        st.plotly_chart(fig_grazing, use_container_width=True)

def visualize_energia():
    """Create visualizations for Energia"""
    df = load_dataframe("energia.csv")
    if df.empty:
        st.warning("No hay datos en la sección Energía para visualizar.")
        return
    
    # Check if we have the required columns
    energy_columns = ['consumo_diesel', 'consumo_gasolina', 'consumo_GNC', 'consumo_electricidad']
    if not all(col in df.columns for col in energy_columns):
        st.warning("Faltan datos de consumo energético para visualizar correctamente.")
        return
    
    # Create energy consumption summary
    energy_data = pd.DataFrame({
        'Tipo': ['Diesel (L)', 'Gasolina (L)', 'GNC (m³)', 'Electricidad (kWh)'],
        'Consumo': [
            df['consumo_diesel'].iloc[0], 
            df['consumo_gasolina'].iloc[0], 
            df['consumo_GNC'].iloc[0], 
            df['consumo_electricidad'].iloc[0]
        ]
    })
    
    fig_energy = create_bar_chart(energy_data, 'Tipo', 'Consumo', 'Consumo Energético Anual')
    st.plotly_chart(fig_energy, use_container_width=True)
    
    # Calculate approximate equivalent CO2 emissions
    # These are rough conversion factors for illustration
    co2_data = pd.DataFrame({
        'Fuente': ['Diesel', 'Gasolina', 'GNC', 'Electricidad'],
        'CO2 (kg)': [
            df['consumo_diesel'].iloc[0] * 2.68,  # kg CO2 per L of diesel
            df['consumo_gasolina'].iloc[0] * 2.31,  # kg CO2 per L of gasoline
            df['consumo_GNC'].iloc[0] * 1.86,  # kg CO2 per m³ of CNG
            df['consumo_electricidad'].iloc[0] * 0.38  # kg CO2 per kWh (varies by country)
        ]
    })
    
    fig_co2 = create_pie_chart(co2_data, 'Fuente', 'CO2 (kg)', 'Emisiones Aproximadas de CO2 por Fuente')
    st.plotly_chart(fig_co2, use_container_width=True)

def visualize_superficies():
    """Create visualizations for Superficies e Insumos"""
    df = load_dataframe("superficies_insumos.csv")
    if df.empty:
        st.warning("No hay datos en la sección Superficies e Insumos para visualizar.")
        return
    
    if 'cultivo' in df.columns and 'hectareas' in df.columns:
        fig_area = create_pie_chart(df, 'cultivo', 'hectareas', 'Distribución de Área por Cultivo')
        st.plotly_chart(fig_area, use_container_width=True)
    
    if 'cultivo' in df.columns and 'productividad_materia_verde' in df.columns:
        fig_productivity = create_bar_chart(
            df, 
            'cultivo', 
            'productividad_materia_verde', 
            'Productividad por Cultivo (kg/ha)'
        )
        st.plotly_chart(fig_productivity, use_container_width=True)
    
    if 'temporada' in df.columns and 'hectareas' in df.columns:
        # Group by season
        season_data = df.groupby('temporada')['hectareas'].sum().reset_index()
        fig_season = create_pie_chart(
            season_data, 
            'temporada', 
            'hectareas', 
            'Distribución de Área por Temporada'
        )
        st.plotly_chart(fig_season, use_container_width=True)
