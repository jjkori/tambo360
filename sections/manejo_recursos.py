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
    
    # Track form submission state
    if "show_manejo_summary" not in st.session_state:
        st.session_state.show_manejo_summary = False
    
    # Store form data temporarily
    if "manejo_temp_data" not in st.session_state:
        st.session_state.manejo_temp_data = {}
    
    # Handle confirmation
    if st.session_state.show_manejo_summary:
        # Get the temporary data
        data = st.session_state.manejo_temp_data
        
        # Display confirmation summary in a nice format with green checkmark
        st.markdown("### ✅ Resumen de Manejo y Recursos")
        
        # Create a formatted summary
        st.markdown(f"""
        ##### Tipo de Labranza
        * **Tipo de Labranza**: {data['tipo_labranza']}
        
        ##### Proporción de Cobertura
        * **Con Cobertura**: {data['proporcion_cobertura']}%
        * **Sin Cobertura**: {data['proporcion_sin_cobertura']}%
        
        ##### Cambios en el Suelo
        * **Cambios en el Suelo**: {data['cambios_suelo']}
        * **Año del Cambio**: {data['anno_cambio'] if data['anno_cambio'] else "No especificado"}
        """)
        
        # Add confirmation button
        if st.button("📝 Confirmar y guardar", key="confirm_manejo", type="primary"):
            # Create dataframe
            new_df = pd.DataFrame([data])
            
            # Save dataframe
            save_dataframe(new_df, "manejo.csv")
            
            # Generate new UUID for next entry
            st.session_state.manejo_uuid = generate_uuid()
            
            # Reset the summary view
            st.session_state.show_manejo_summary = False
            st.session_state.manejo_temp_data = {}
            
            # Show success message
            show_success_message("Datos guardados correctamente")
            
            # Rerun to refresh the app
            st.rerun()
        
        # Add back button
        if st.button("↩ Volver y editar", key="back_manejo"):
            st.session_state.show_manejo_summary = False
            st.rerun()
            
        # Add divider
        st.divider()
    
    # Only show the form if we're not in summary mode
    if not st.session_state.show_manejo_summary:
        # Initialize form values
        if has_existing_data and not st.session_state.manejo_temp_data:
            # Get the most recent entry
            latest_data = df.iloc[-1]
            
            # Pre-fill form fields
            tipo_labranza = latest_data.get('tipo_labranza', "Siembra directa")
            proporcion_cobertura = latest_data.get('proporcion_cobertura', 50)
            proporcion_sin_cobertura = latest_data.get('proporcion_sin_cobertura', 50)
            cambios_suelo = latest_data.get('cambios_suelo', "No hay cambios")
            anno_cambio = latest_data.get('anno_cambio', None)
        elif st.session_state.manejo_temp_data:
            # Get data from session state if we're coming back from summary
            data = st.session_state.manejo_temp_data
            tipo_labranza = data.get('tipo_labranza', "Siembra directa")
            proporcion_cobertura = data.get('proporcion_cobertura', 50)
            proporcion_sin_cobertura = data.get('proporcion_sin_cobertura', 50)
            cambios_suelo = data.get('cambios_suelo', "No hay cambios")
            anno_cambio = data.get('anno_cambio', None)
        else:
            # Default values for new entry
            tipo_labranza = "Siembra directa"
            proporcion_cobertura = 50
            proporcion_sin_cobertura = 50
            cambios_suelo = "No hay cambios"
            anno_cambio = None
        
        # Create form
        with st.form("manejo_form"):
            st.subheader("Tipo de Labranza")
            
            tipo_labranza = st.selectbox("Tipo de Labranza", 
                                      options=["Siembra directa", "Mínima", "Convencional", "Otro"],
                                      index=["Siembra directa", "Mínima", "Convencional", "Otro"].index(tipo_labranza) if tipo_labranza in ["Siembra directa", "Mínima", "Convencional", "Otro"] else 0)
            
            st.subheader("Proporción de Cobertura")
            col1, col2 = st.columns(2)
            
            with col1:
                proporcion_cobertura = st.number_input("Con Cobertura (%)", min_value=0, max_value=100, value=proporcion_cobertura)
            
            with col2:
                # Calculate the remaining percentage for no coverage
                proporcion_sin_cobertura = 100 - proporcion_cobertura
                st.metric("Sin Cobertura (%)", f"{proporcion_sin_cobertura}%")
                
                # Check if percentages sum to 100
                if proporcion_cobertura > 100:
                    st.warning("⚠️ La proporción de cobertura no puede superar 100%")
            
            st.subheader("Cambios en el Suelo")
            col1, col2 = st.columns(2)
            
            with col1:
                cambios_suelo = st.selectbox("Cambios en el Suelo", 
                                         options=["No hay cambios", "Conversión a pradera", "Conversión a cultivo", "Otro"],
                                         index=["No hay cambios", "Conversión a pradera", "Conversión a cultivo", "Otro"].index(cambios_suelo) if cambios_suelo in ["No hay cambios", "Conversión a pradera", "Conversión a cultivo", "Otro"] else 0)
            
            with col2:
                # Only show year input if there are changes
                if cambios_suelo != "No hay cambios":
                    current_year = pd.Timestamp.now().year
                    anno_cambio = st.number_input("Año del Cambio", min_value=1980, max_value=current_year, value=anno_cambio if anno_cambio else current_year)
                else:
                    anno_cambio = None
            
            submitted = st.form_submit_button("Revisar información antes de guardar")
            
            if submitted:
                # Validate input
                validation_errors = []
                
                if not validate_percentage(proporcion_cobertura):
                    validation_errors.append("La proporción de cobertura debe ser un valor entre 0 y 100.")
                
                if cambios_suelo != "No hay cambios" and anno_cambio is None:
                    validation_errors.append("Si hay cambios en el suelo, debe especificar el año del cambio.")
                
                # If there are validation errors, display them and stop
                if validation_errors:
                    for error in validation_errors:
                        show_validation_error(error)
                    return
                
                # Store data temporarily in session state
                st.session_state.manejo_temp_data = {
                    'uuid': st.session_state.manejo_uuid,
                    'tipo_labranza': tipo_labranza,
                    'proporcion_cobertura': proporcion_cobertura,
                    'proporcion_sin_cobertura': proporcion_sin_cobertura,
                    'cambios_suelo': cambios_suelo,
                    'anno_cambio': anno_cambio
                }
                
                # Show summary for confirmation
                st.session_state.show_manejo_summary = True
                
                # Rerun to show the summary
                st.rerun()
    
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