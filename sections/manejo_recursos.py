import streamlit as st
import pandas as pd
from utils import save_dataframe, load_dataframe, validate_numeric, validate_percentage, validate_text, generate_uuid, show_validation_error, show_success_message

def show_manejo_recursos():
    """Display and handle the Manejo y Recursos form"""
    st.title("Manejo y Recursos")
    
    # Check if we have existing data
    df = load_dataframe("manejo.csv")
    has_existing_data = not df.empty
    
    # Generate UUID if not present
    if "manejo_uuid" not in st.session_state:
        st.session_state.manejo_uuid = generate_uuid()
    
    # Create form
    with st.form("manejo_recursos_form"):
        st.subheader("Manejo de Suelo")
        col1, col2 = st.columns(2)
        
        with col1:
            tipo_labranza = st.selectbox("Tipo de Labranza", options=["Convencional", "Reducida", "Directa"])
            proporcion_cobertura = st.number_input("Proporción Cobertura (%)", min_value=0, max_value=100, value=0)
        
        with col2:
            proporcion_sin_cobertura = st.number_input("Proporción Suelo Sin Cobertura (%)", min_value=0, max_value=100, value=0)
            
            # Check if percentages sum to 100
            if proporcion_cobertura + proporcion_sin_cobertura != 100:
                st.warning("⚠️ La suma de los porcentajes debe ser 100%")
        
        st.subheader("Cambios en Manejo de Suelos")
        col1, col2 = st.columns(2)
        
        with col1:
            manejo_suelos_cambios = st.selectbox("¿Ha realizado cambios en el manejo de suelos?", options=["No", "Sí"])
        
        with col2:
            año_cambio_manejo = st.number_input("Año del Cambio", min_value=2000, max_value=2100, value=2023, disabled=manejo_suelos_cambios=="No")
        
        submitted = st.form_submit_button("Guardar Información de Manejo y Recursos")
        
        if submitted:
            # Validate input
            validation_errors = []
            
            if not validate_percentage(proporcion_cobertura):
                validation_errors.append("La proporción de cobertura debe ser un porcentaje válido (0-100).")
            
            if not validate_percentage(proporcion_sin_cobertura):
                validation_errors.append("La proporción sin cobertura debe ser un porcentaje válido (0-100).")
            
            if proporcion_cobertura + proporcion_sin_cobertura != 100:
                validation_errors.append("La suma de las proporciones de cobertura debe ser 100%.")
            
            # If there are validation errors, display them and stop
            if validation_errors:
                for error in validation_errors:
                    show_validation_error(error)
                return
            
            # Create data object
            data = {
                'uuid': st.session_state.manejo_uuid,
                'tipo_labranza': tipo_labranza,
                'proporción_cobertura': proporcion_cobertura,
                'proporción_suelo_sin_cobertura': proporcion_sin_cobertura,
                'manejo_suelos_cambios': manejo_suelos_cambios,
                'año_cambio_manejo': año_cambio_manejo if manejo_suelos_cambios == "Sí" else None
            }
            
            # Create dataframe
            new_df = pd.DataFrame([data])
            
            # Save dataframe
            save_dataframe(new_df, "manejo.csv")
            
            # Generate new UUID for next entry
            st.session_state.manejo_uuid = generate_uuid()
            
            # Show success message
            show_success_message("Datos guardados correctamente")
    
    # Show existing data if available
    if has_existing_data:
        st.subheader("Datos actuales de Manejo y Recursos")
        display_df = df.drop(columns=['uuid']) if 'uuid' in df.columns else df
        st.dataframe(display_df)
        
        # Allow deletion of entries
        if st.button("Eliminar Última Entrada"):
            if len(df) > 0:
                df = df.iloc[:-1]
                df.to_csv("data/manejo.csv", index=False)
                st.success("Última entrada eliminada. Recarga la página para ver los cambios.")
                st.rerun()
