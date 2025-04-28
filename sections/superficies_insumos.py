import streamlit as st
import pandas as pd
from utils import save_dataframe, load_dataframe, validate_numeric, validate_text, generate_uuid, show_validation_error, show_success_message

def show_superficies_insumos():
    """Display and handle the Superficies e Insumos form"""
    st.title("Superficies e Insumos")
    
    # Check if we have existing data
    df = load_dataframe("superficies_insumos.csv")
    has_existing_data = not df.empty
    
    # Generate UUID if not present
    if "superficies_uuid" not in st.session_state:
        st.session_state.superficies_uuid = generate_uuid()
    
    # Create form
    with st.form("superficies_insumos_form"):
        st.subheader("Información de Cultivo")
        col1, col2 = st.columns(2)
        
        with col1:
            cultivo = st.text_input("Cultivo/Pastura")
            temporada = st.selectbox("Temporada", options=["Invierno", "Verano", "Anual"])
        
        with col2:
            hectareas = st.number_input("Hectáreas", min_value=0.0, format="%.2f")
            productividad_materia_verde = st.number_input("Productividad Materia Verde (kg/ha)", min_value=0)
        
        st.subheader("Información de Residuos")
        col1, col2 = st.columns(2)
        
        with col1:
            residuos_generados = st.number_input("Residuos Generados (kg/ha)", min_value=0)
        
        with col2:
            destino_options = ["Incorporación al suelo", "Quema", "Recolección", "Almacenamiento", "Compostaje", "Otro"]
            destino_residuos = st.selectbox("Destino de Residuos", options=destino_options)
        
        submitted = st.form_submit_button("Guardar Información de Superficies e Insumos")
        
        if submitted:
            # Validate input
            validation_errors = []
            
            if not validate_text(cultivo):
                validation_errors.append("El nombre del cultivo/pastura es obligatorio.")
            
            if not validate_numeric(hectareas, min_val=0):
                validation_errors.append("Las hectáreas deben ser un número positivo.")
            
            if not validate_numeric(productividad_materia_verde, min_val=0):
                validation_errors.append("La productividad debe ser un número positivo.")
            
            if not validate_numeric(residuos_generados, min_val=0):
                validation_errors.append("Los residuos generados deben ser un número positivo.")
            
            # If there are validation errors, display them and stop
            if validation_errors:
                for error in validation_errors:
                    show_validation_error(error)
                return
            
            # Create data object
            data = {
                'uuid': st.session_state.superficies_uuid,
                'cultivo': cultivo,
                'temporada': temporada,
                'hectareas': hectareas,
                'productividad_materia_verde': productividad_materia_verde,
                'residuos_generados': residuos_generados,
                'destino_residuos': destino_residuos
            }
            
            # Create dataframe
            new_df = pd.DataFrame([data])
            
            # Save dataframe
            save_dataframe(new_df, "superficies_insumos.csv")
            
            # Generate new UUID for next entry
            st.session_state.superficies_uuid = generate_uuid()
            
            # Show success message
            show_success_message("Datos guardados correctamente")
            
            # Clear form (hack: rerun the app)
            st.rerun()
    
    # Show existing data if available
    if has_existing_data:
        st.subheader("Datos actuales de Superficies e Insumos")
        display_df = df.drop(columns=['uuid']) if 'uuid' in df.columns else df
        st.dataframe(display_df)
        
        # Summary
        st.subheader("Resumen")
        total_area = df['hectareas'].sum()
        st.metric("Superficie Total Registrada", f"{total_area:.2f} ha")
        
        # Allow deletion of entries
        if st.button("Eliminar Última Entrada"):
            if len(df) > 0:
                df = df.iloc[:-1]
                df.to_csv("data/superficies_insumos.csv", index=False)
                st.success("Última entrada eliminada. Recarga la página para ver los cambios.")
                st.rerun()
