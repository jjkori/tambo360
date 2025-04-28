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
    
    # Track form submission state
    if "show_superficies_summary" not in st.session_state:
        st.session_state.show_superficies_summary = False
    
    # Store form data temporarily
    if "superficies_temp_data" not in st.session_state:
        st.session_state.superficies_temp_data = {}
    
    # Handle confirmation
    if st.session_state.show_superficies_summary:
        # Get the temporary data
        data = st.session_state.superficies_temp_data
        
        # Display confirmation summary in a nice format with green checkmark
        st.markdown("### ✅ Resumen de superficies")
        
        # Create a formatted summary
        st.markdown(f"""
        * **Cultivo/Pastura**: {data['cultivo']}
        * **Temporada**: {data['temporada']}
        * **Hectáreas**: {data['hectareas']:.2f} ha
        * **Productividad Materia Verde**: {data['productividad_materia_verde']} kg/ha
        * **Residuos Generados**: {data['residuos_generados']} kg/ha
        * **Destino de Residuos**: {data['destino_residuos']}
        """)
        
        # Calculate total production
        total_production = data['hectareas'] * data['productividad_materia_verde']
        st.markdown(f"* **Producción Total Estimada**: {total_production:.2f} kg")
        
        # Add confirmation button
        if st.button("📝 Confirmar y guardar", key="confirm_superficies", type="primary"):
            # Create dataframe
            new_df = pd.DataFrame([data])
            
            # Save dataframe
            save_dataframe(new_df, "superficies_insumos.csv")
            
            # Generate new UUID for next entry
            st.session_state.superficies_uuid = generate_uuid()
            
            # Reset the summary view
            st.session_state.show_superficies_summary = False
            st.session_state.superficies_temp_data = {}
            
            # Show success message
            show_success_message("Datos guardados correctamente")
            
            # Rerun to refresh the app
            st.rerun()
        
        # Add back button
        if st.button("↩ Volver y editar", key="back_superficies"):
            st.session_state.show_superficies_summary = False
            st.rerun()
            
        # Add divider
        st.divider()
    
    # Only show the form if we're not in summary mode
    if not st.session_state.show_superficies_summary:
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
            
            submitted = st.form_submit_button("Revisar información antes de guardar")
            
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
                
                # Store data temporarily in session state
                st.session_state.superficies_temp_data = {
                    'uuid': st.session_state.superficies_uuid,
                    'cultivo': cultivo,
                    'temporada': temporada,
                    'hectareas': hectareas,
                    'productividad_materia_verde': productividad_materia_verde,
                    'residuos_generados': residuos_generados,
                    'destino_residuos': destino_residuos
                }
                
                # Show summary for confirmation
                st.session_state.show_superficies_summary = True
                
                # Rerun to show the summary
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
        
        # Group by cultivo and sum hectareas
        if len(df) > 1:
            cultivo_summary = df.groupby('cultivo')['hectareas'].sum().reset_index()
            cultivo_summary.columns = ['Cultivo/Pastura', 'Hectáreas']
            st.subheader("Distribución por Cultivo/Pastura")
            st.dataframe(cultivo_summary)
        
        # Allow deletion of entries
        if st.button("Eliminar Última Entrada"):
            if len(df) > 0:
                df = df.iloc[:-1]
                df.to_csv("data/superficies_insumos.csv", index=False)
                st.success("Última entrada eliminada. Recarga la página para ver los cambios.")
                st.rerun()
