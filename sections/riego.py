import streamlit as st
import pandas as pd
from utils import save_dataframe, load_dataframe, validate_numeric, validate_percentage, validate_text, generate_uuid, show_validation_error, show_success_message

def show_riego():
    """Display and handle the Riego / Uso de Agua form"""
    st.title("Riego / Uso de Agua")
    
    # Check if we have existing data
    df = load_dataframe("riego.csv")
    has_existing_data = not df.empty
    
    # Generate UUID if not present
    if "riego_uuid" not in st.session_state:
        st.session_state.riego_uuid = generate_uuid()
    
    # Create form
    with st.form("riego_form"):
        st.subheader("Fuente de Agua")
        col1, col2 = st.columns(2)
        
        with col1:
            tipo_fuente = st.selectbox("Tipo de Fuente", 
                                     options=["Pozo", "Río", "Canal", "Otro"])
            consumo_total = st.number_input("Consumo Total (m³/año)", min_value=0)
        
        with col2:
            uso_para_bebida = st.number_input("Uso para Bebida (%)", min_value=0, max_value=100, value=0)
            uso_para_limpieza = st.number_input("Uso para Limpieza (%)", min_value=0, max_value=100, value=0)
            
            # Calculate the remaining percentage for irrigation
            uso_para_riego = 100 - uso_para_bebida - uso_para_limpieza
            st.metric("Uso para Riego (%)", f"{uso_para_riego}%")
            
            # Check if percentages sum to 100
            if uso_para_bebida + uso_para_limpieza > 100:
                st.warning("⚠️ La suma de los porcentajes no puede superar 100%")
        
        st.subheader("Permisos y Monitoreo")
        col1, col2 = st.columns(2)
        
        with col1:
            permiso_agua = st.selectbox("¿Tiene Permiso de Agua?", options=["No", "Sí"])
        
        with col2:
            monitoreo_riego = st.selectbox("¿Realiza Monitoreo de Riego?", options=["No", "Sí"])
        
        eventos_riego = st.text_area("Eventos de Riego (breve descripción)")
        
        submitted = st.form_submit_button("Guardar Información de Riego / Uso de Agua")
        
        if submitted:
            # Validate input
            validation_errors = []
            
            if not validate_numeric(consumo_total, min_val=0):
                validation_errors.append("El consumo total debe ser un número positivo.")
            
            if not validate_percentage(uso_para_bebida):
                validation_errors.append("El uso para bebida debe ser un porcentaje válido (0-100).")
            
            if not validate_percentage(uso_para_limpieza):
                validation_errors.append("El uso para limpieza debe ser un porcentaje válido (0-100).")
            
            if uso_para_bebida + uso_para_limpieza > 100:
                validation_errors.append("La suma de los porcentajes de uso no puede superar 100%.")
            
            # If there are validation errors, display them and stop
            if validation_errors:
                for error in validation_errors:
                    show_validation_error(error)
                return
            
            # Create data object
            data = {
                'uuid': st.session_state.riego_uuid,
                'tipo_fuente': tipo_fuente,
                'consumo_total': consumo_total,
                'uso_para_bebida': uso_para_bebida,
                'uso_para_limpieza': uso_para_limpieza,
                'uso_para_riego': uso_para_riego,
                'permiso_agua': permiso_agua,
                'monitoreo_riego': monitoreo_riego,
                'eventos_riego': eventos_riego
            }
            
            # Create dataframe
            new_df = pd.DataFrame([data])
            
            # Save dataframe
            save_dataframe(new_df, "riego.csv")
            
            # Generate new UUID for next entry
            st.session_state.riego_uuid = generate_uuid()
            
            # Show success message
            show_success_message("Datos guardados correctamente")
    
    # Show existing data if available
    if has_existing_data:
        st.subheader("Datos actuales de Riego / Uso de Agua")
        display_df = df.drop(columns=['uuid']) if 'uuid' in df.columns else df
        st.dataframe(display_df)
        
        # Allow deletion of entries
        if st.button("Eliminar Última Entrada"):
            if len(df) > 0:
                df = df.iloc[:-1]
                df.to_csv("data/riego.csv", index=False)
                st.success("Última entrada eliminada. Recarga la página para ver los cambios.")
                st.rerun()
