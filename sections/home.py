import streamlit as st

def show_home():
    """Display home page with app information"""
    st.title("FieldLens - Recolección de Datos en Tambos")
    st.subheader("Data collection, reimagined for agriculture")
    
    # App description
    st.markdown("""
    FieldLens es una aplicación diseñada para la recolección eficiente de datos en establecimientos lecheros (tambos).
    
    La información se guarda automáticamente mientras completas cada sección, permitiéndote generar informes detallados
    y visualizar los resultados a través de dashboards interactivos.
    """)
    
    # Quick instructions
    st.subheader("Instrucciones rápidas:")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### 1️⃣")
        st.markdown("Seleccioná una sección en el menú lateral")
    
    with col2:
        st.markdown("### 2️⃣")
        st.markdown("Cargá la información en los formularios")
    
    with col3:
        st.markdown("### 3️⃣")
        st.markdown("Los datos se guardan automáticamente")
    
    with col4:
        st.markdown("### 4️⃣")
        st.markdown("Exportá reportes a Word, PDF o Excel")
    
    # Tips
    st.success("📍 Tip: empezá por 'Datos Generales' si es tu primera vez usando la aplicación.")
    
    # Features
    st.subheader("Funcionalidades principales")
    
    features_col1, features_col2 = st.columns(2)
    
    with features_col1:
        st.markdown("""
        - **Formularios intuitivos** para cada sección
        - **Guardado automático** de la información
        - **Validación de datos** en tiempo real
        - **Cálculos automáticos** de métricas clave
        """)
    
    with features_col2:
        st.markdown("""
        - **Dashboards visuales** para análisis rápido
        - **Exportación profesional** a Word y PDF
        - **Compatibilidad con Excel** para análisis avanzados
        - **Diseño mobile-first** para uso en campo
        """)
    
    # Data collection sections 
    st.subheader("Secciones de recolección de datos")
    
    sections_col1, sections_col2, sections_col3 = st.columns(3)
    
    with sections_col1:
        st.markdown("""
        - 📋 **Datos Generales**
        - 🌱 **Superficies e Insumos**
        - 🛠️ **Manejo y Recursos**
        - 🌿 **Fertilización**
        """)
    
    with sections_col2:
        st.markdown("""
        - 🔒 **Protección de Cultivos**
        - 💧 **Riego / Uso de Agua**
        - ⚡ **Energía**
        - 🐄 **Rebaño**
        """)
    
    with sections_col3:
        st.markdown("""
        - 📊 **Resumen Rebaño**
        - 🧪 **Gestión de Efluentes**
        - 🚚 **Transporte**
        - 📈 **Dashboard General**
        """)
    
    # Footer
    st.markdown("---")
    st.caption("by Cultura CŌW | Design by La Vaca Studio")
