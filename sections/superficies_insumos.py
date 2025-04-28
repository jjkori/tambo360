import streamlit as st
import pandas as pd
from utils import save_dataframe, load_dataframe, validate_numeric, validate_percentage, validate_text, generate_uuid, show_validation_error, show_success_message

def show_superficies_insumos():
    """Display and handle the Superficies e Insumos form"""
    st.title("Superficies e Insumos")
    
    # Check if we have existing data
    df = load_dataframe("superficies_insumos.csv")
    has_existing_data = not df.empty
    
    # Generate UUID if not present
    if "superficie_uuid" not in st.session_state:
        st.session_state.superficie_uuid = generate_uuid()
    
    # Track form submission state
    if "show_superficie_summary" not in st.session_state:
        st.session_state.show_superficie_summary = False
    
    # Store form data temporarily
    if "superficie_temp_data" not in st.session_state:
        st.session_state.superficie_temp_data = {}
    
    # Handle confirmation
    if st.session_state.show_superficie_summary:
        # Get the temporary data
        data = st.session_state.superficie_temp_data
        
        # Display confirmation summary in a nice format with green checkmark
        st.markdown("### ✅ Resumen de Superficies e Insumos")
        
        # Create a formatted summary
        st.markdown(f"""
        ##### Información General
        * **Cultivo**: {data['cultivo']}
        * **Temporada**: {data['temporada']}
        * **Hectáreas**: {data['hectareas']} ha
        
        ##### Productividad y Residuos
        * **Productividad de Materia Verde**: {data['productividad_materia_verde']} kg/ha
        * **Residuos Generados**: {data['residuos_generados']} toneladas
        * **Destino de Residuos**: {data['destino_residuos']}
        """)
        
        # Add confirmation button
        if st.button("📝 Confirmar y guardar", key="confirm_superficie", type="primary"):
            # Create dataframe
            new_df = pd.DataFrame([data])
            
            # Save dataframe
            save_dataframe(new_df, "superficies_insumos.csv")
            
            # Generate new UUID for next entry
            st.session_state.superficie_uuid = generate_uuid()
            
            # Reset the summary view
            st.session_state.show_superficie_summary = False
            st.session_state.superficie_temp_data = {}
            
            # Show success message
            show_success_message("Datos guardados correctamente")
            
            # Rerun to refresh the app
            st.rerun()
        
        # Add back button
        if st.button("↩ Volver y editar", key="back_superficie"):
            st.session_state.show_superficie_summary = False
            st.rerun()
            
        # Add divider
        st.divider()
    
    # Only show the form if we're not in summary mode
    if not st.session_state.show_superficie_summary:
        # Initialize form values
        if has_existing_data and not st.session_state.superficie_temp_data:
            # Get the most recent entry
            latest_data = df.iloc[-1]
            
            # Pre-fill form fields
            cultivo = latest_data.get('cultivo', "")
            temporada = latest_data.get('temporada', "Verano")
            hectareas = latest_data.get('hectareas', 0.0)
            productividad_materia_verde = latest_data.get('productividad_materia_verde', 0.0)
            residuos_generados = latest_data.get('residuos_generados', 0.0)
            destino_residuos = latest_data.get('destino_residuos', "Incorporación")
        elif st.session_state.superficie_temp_data:
            # Get data from session state if we're coming back from summary
            data = st.session_state.superficie_temp_data
            cultivo = data.get('cultivo', "")
            temporada = data.get('temporada', "Verano")
            hectareas = data.get('hectareas', 0.0)
            productividad_materia_verde = data.get('productividad_materia_verde', 0.0)
            residuos_generados = data.get('residuos_generados', 0.0)
            destino_residuos = data.get('destino_residuos', "Incorporación")
        else:
            # Default values for new entry
            cultivo = ""
            temporada = "Verano"
            hectareas = 0.0
            productividad_materia_verde = 0.0
            residuos_generados = 0.0
            destino_residuos = "Incorporación"
        
        # Create form
        with st.form("superficie_form"):
            st.subheader("Información General")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                cultivo = st.text_input("Cultivo", value=cultivo)
            
            with col2:
                temporada = st.selectbox("Temporada", 
                                     options=["Verano", "Invierno", "Primavera", "Otoño", "Todo el año"],
                                     index=["Verano", "Invierno", "Primavera", "Otoño", "Todo el año"].index(temporada) if temporada in ["Verano", "Invierno", "Primavera", "Otoño", "Todo el año"] else 0)
            
            with col3:
                hectareas = st.number_input("Hectáreas", min_value=0.0, step=0.01, value=float(hectareas))
            
            st.subheader("Productividad y Residuos")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                productividad_materia_verde = st.number_input("Productividad de Materia Verde (kg/ha)", 
                                                         min_value=0.0, step=100.0,
                                                         value=float(productividad_materia_verde))
            
            with col2:
                residuos_generados = st.number_input("Residuos Generados (toneladas)", 
                                                min_value=0.0, step=0.1,
                                                value=float(residuos_generados))
            
            with col3:
                destino_residuos = st.selectbox("Destino de Residuos", 
                                            options=["Incorporación", "Recolección", "Quema", "Compostaje", "Otro"],
                                            index=["Incorporación", "Recolección", "Quema", "Compostaje", "Otro"].index(destino_residuos) if destino_residuos in ["Incorporación", "Recolección", "Quema", "Compostaje", "Otro"] else 0)
            
            submitted = st.form_submit_button("Revisar información antes de guardar")
            
            if submitted:
                # Validate input
                validation_errors = []
                
                if not validate_text(cultivo, min_length=1):
                    validation_errors.append("El cultivo no puede estar vacío.")
                
                if not validate_numeric(hectareas, min_val=0):
                    validation_errors.append("Las hectáreas deben ser un número positivo.")
                
                if not validate_numeric(productividad_materia_verde, min_val=0):
                    validation_errors.append("La productividad de materia verde debe ser un número positivo.")
                
                if not validate_numeric(residuos_generados, min_val=0):
                    validation_errors.append("Los residuos generados deben ser un número positivo.")
                
                # If there are validation errors, display them and stop
                if validation_errors:
                    for error in validation_errors:
                        show_validation_error(error)
                    return
                
                # Store data temporarily in session state
                st.session_state.superficie_temp_data = {
                    'uuid': st.session_state.superficie_uuid,
                    'cultivo': cultivo,
                    'temporada': temporada,
                    'hectareas': hectareas,
                    'productividad_materia_verde': productividad_materia_verde,
                    'residuos_generados': residuos_generados,
                    'destino_residuos': destino_residuos
                }
                
                # Show summary for confirmation
                st.session_state.show_superficie_summary = True
                
                # Rerun to show the summary
                st.rerun()
    
    # Show existing data if available
    if has_existing_data:
        st.subheader("Datos actuales de Superficies e Insumos")
        display_df = df.drop(columns=['uuid']) if 'uuid' in df.columns else df
        st.dataframe(display_df)
        
        # Allow deletion of entries
        if st.button("Eliminar Última Entrada"):
            if len(df) > 0:
                df = df.iloc[:-1]
                df.to_csv("data/superficies_insumos.csv", index=False)
                st.success("Última entrada eliminada. Recarga la página para ver los cambios.")
                st.rerun()