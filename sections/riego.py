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
    
    # Track form submission state
    if "show_riego_summary" not in st.session_state:
        st.session_state.show_riego_summary = False
    
    # Store form data temporarily
    if "riego_temp_data" not in st.session_state:
        st.session_state.riego_temp_data = {}
    
    # Handle confirmation
    if st.session_state.show_riego_summary:
        # Get the temporary data
        data = st.session_state.riego_temp_data
        
        # Display confirmation summary in a nice format with green checkmark
        st.markdown("### ✅ Resumen de Riego / Uso de Agua")
        
        # Create a formatted summary
        st.markdown(f"""
        ##### Fuente de Agua
        * **Tipo de Fuente**: {data['tipo_fuente']}
        * **Consumo Total**: {data['consumo_total']} m³/año
        
        ##### Distribución de Uso
        * **Uso para Bebida**: {data['uso_para_bebida']}%
        * **Uso para Limpieza**: {data['uso_para_limpieza']}%
        * **Uso para Riego**: {data['uso_para_riego']}%
        
        ##### Permisos y Monitoreo
        * **Permiso de Agua**: {data['permiso_agua']}
        * **Monitoreo de Riego**: {data['monitoreo_riego']}
        """)
        
        # Add events information if provided
        if data['eventos_riego']:
            st.markdown(f"""
            ##### Eventos de Riego
            {data['eventos_riego']}
            """)
        
        # Add confirmation button
        if st.button("📝 Confirmar y guardar", key="confirm_riego", type="primary"):
            # Create dataframe
            new_df = pd.DataFrame([data])
            
            # Save dataframe
            save_dataframe(new_df, "riego.csv")
            
            # Generate new UUID for next entry
            st.session_state.riego_uuid = generate_uuid()
            
            # Reset the summary view
            st.session_state.show_riego_summary = False
            st.session_state.riego_temp_data = {}
            
            # Show success message
            show_success_message("Datos guardados correctamente")
            
            # Rerun to refresh the app
            st.rerun()
        
        # Add back button
        if st.button("↩ Volver y editar", key="back_riego"):
            st.session_state.show_riego_summary = False
            st.rerun()
            
        # Add divider
        st.divider()
    
    # Only show the form if we're not in summary mode
    if not st.session_state.show_riego_summary:
        # Initialize form values
        if has_existing_data and not st.session_state.riego_temp_data:
            # Get the most recent entry
            latest_data = df.iloc[-1]
            
            # Pre-fill form fields
            tipo_fuente = latest_data.get('tipo_fuente', "Pozo")
            consumo_total = latest_data.get('consumo_total', 0)
            uso_para_bebida = latest_data.get('uso_para_bebida', 0)
            uso_para_limpieza = latest_data.get('uso_para_limpieza', 0)
            uso_para_riego = latest_data.get('uso_para_riego', 0)
            permiso_agua = latest_data.get('permiso_agua', "No")
            monitoreo_riego = latest_data.get('monitoreo_riego', "No")
            eventos_riego = latest_data.get('eventos_riego', "")
        elif st.session_state.riego_temp_data:
            # Get data from session state if we're coming back from summary
            data = st.session_state.riego_temp_data
            tipo_fuente = data.get('tipo_fuente', "Pozo")
            consumo_total = data.get('consumo_total', 0)
            uso_para_bebida = data.get('uso_para_bebida', 0)
            uso_para_limpieza = data.get('uso_para_limpieza', 0)
            uso_para_riego = data.get('uso_para_riego', 0)
            permiso_agua = data.get('permiso_agua', "No")
            monitoreo_riego = data.get('monitoreo_riego', "No")
            eventos_riego = data.get('eventos_riego', "")
        else:
            # Default values for new entry
            tipo_fuente = "Pozo"
            consumo_total = 0
            uso_para_bebida = 0
            uso_para_limpieza = 0
            uso_para_riego = 100
            permiso_agua = "No"
            monitoreo_riego = "No"
            eventos_riego = ""
        
        # Create form
        with st.form("riego_form"):
            st.subheader("Fuente de Agua")
            col1, col2 = st.columns(2)
            
            with col1:
                tipo_fuente = st.selectbox("Tipo de Fuente", 
                                         options=["Pozo", "Río", "Canal", "Otro"],
                                         index=["Pozo", "Río", "Canal", "Otro"].index(tipo_fuente) if tipo_fuente in ["Pozo", "Río", "Canal", "Otro"] else 0)
                consumo_total = st.number_input("Consumo Total (m³/año)", min_value=0, value=consumo_total)
            
            with col2:
                uso_para_bebida = st.number_input("Uso para Bebida (%)", min_value=0, max_value=100, value=uso_para_bebida)
                uso_para_limpieza = st.number_input("Uso para Limpieza (%)", min_value=0, max_value=100, value=uso_para_limpieza)
                
                # Calculate the remaining percentage for irrigation
                uso_para_riego = 100 - uso_para_bebida - uso_para_limpieza
                st.metric("Uso para Riego (%)", f"{uso_para_riego}%")
                
                # Check if percentages sum to 100
                if uso_para_bebida + uso_para_limpieza > 100:
                    st.warning("⚠️ La suma de los porcentajes no puede superar 100%")
            
            st.subheader("Permisos y Monitoreo")
            col1, col2 = st.columns(2)
            
            with col1:
                permiso_agua = st.selectbox("¿Tiene Permiso de Agua?", options=["No", "Sí"], 
                                         index=0 if permiso_agua == "No" else 1)
            
            with col2:
                monitoreo_riego = st.selectbox("¿Realiza Monitoreo de Riego?", options=["No", "Sí"],
                                           index=0 if monitoreo_riego == "No" else 1)
            
            eventos_riego = st.text_area("Eventos de Riego (breve descripción)", value=eventos_riego)
            
            submitted = st.form_submit_button("Revisar información antes de guardar")
            
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
                
                # Store data temporarily in session state
                st.session_state.riego_temp_data = {
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
                
                # Show summary for confirmation
                st.session_state.show_riego_summary = True
                
                # Rerun to show the summary
                st.rerun()
    
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