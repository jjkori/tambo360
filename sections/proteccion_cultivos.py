import streamlit as st
import pandas as pd
from utils import save_dataframe, load_dataframe, validate_numeric, validate_percentage, validate_text, generate_uuid, show_validation_error, show_success_message

def show_proteccion_cultivos():
    """Display and handle the Protección de Cultivos form"""
    st.title("Protección de Cultivos")
    
    # Check if we have existing data
    df = load_dataframe("proteccion_cultivos.csv")
    has_existing_data = not df.empty
    
    # Generate UUID if not present
    if "proteccion_uuid" not in st.session_state:
        st.session_state.proteccion_uuid = generate_uuid()
    
    # Track form submission state
    if "show_proteccion_summary" not in st.session_state:
        st.session_state.show_proteccion_summary = False
    
    # Store form data temporarily
    if "proteccion_temp_data" not in st.session_state:
        st.session_state.proteccion_temp_data = {}
    
    # Handle confirmation
    if st.session_state.show_proteccion_summary:
        # Get the temporary data
        data = st.session_state.proteccion_temp_data
        
        # Display confirmation summary in a nice format with green checkmark
        st.markdown("### ✅ Resumen de Protección de Cultivos")
        
        # Create a formatted summary
        st.markdown(f"""
        ##### Información General
        * **Área Tratada**: {data['area']}
        * **Producto**: {data['producto']}
        * **Categoría**: {data['categoria']}
        * **Tipo de Aplicación**: {data['tipo_aplicacion']}
        
        ##### Detalles Técnicos
        * **Ingrediente Activo**: {data['ingrediente_activo']}
        * **Porcentaje del Ingrediente Activo**: {data['porcentaje_ingrediente_activo']}%
        * **Dosis Aplicada**: {data['dosis']} kg/ha o L/ha
        """)
        
        # Add confirmation button
        if st.button("📝 Confirmar y guardar", key="confirm_proteccion", type="primary"):
            # Create dataframe
            new_df = pd.DataFrame([data])
            
            # Save dataframe
            save_dataframe(new_df, "proteccion_cultivos.csv")
            
            # Generate new UUID for next entry
            st.session_state.proteccion_uuid = generate_uuid()
            
            # Reset the summary view
            st.session_state.show_proteccion_summary = False
            st.session_state.proteccion_temp_data = {}
            
            # Show success message
            show_success_message("Datos guardados correctamente")
            
            # Rerun to refresh the app
            st.rerun()
        
        # Add back button
        if st.button("↩ Volver y editar", key="back_proteccion"):
            st.session_state.show_proteccion_summary = False
            st.rerun()
            
        # Add divider
        st.divider()
    
    # Only show the form if we're not in summary mode
    if not st.session_state.show_proteccion_summary:
        # Initialize form values
        if has_existing_data and not st.session_state.proteccion_temp_data:
            # Get the most recent entry
            latest_data = df.iloc[-1]
            
            # Pre-fill form fields
            area = latest_data.get('area', "")
            producto = latest_data.get('producto', "")
            categoria = latest_data.get('categoria', "Herbicida")
            tipo_aplicacion = latest_data.get('tipo_aplicacion', "Pulverización")
            ingrediente_activo = latest_data.get('ingrediente_activo', "")
            porcentaje_ingrediente_activo = latest_data.get('porcentaje_ingrediente_activo', 0)
            dosis = latest_data.get('dosis', 0)
        elif st.session_state.proteccion_temp_data:
            # Get data from session state if we're coming back from summary
            data = st.session_state.proteccion_temp_data
            area = data.get('area', "")
            producto = data.get('producto', "")
            categoria = data.get('categoria', "Herbicida")
            tipo_aplicacion = data.get('tipo_aplicacion', "Pulverización")
            ingrediente_activo = data.get('ingrediente_activo', "")
            porcentaje_ingrediente_activo = data.get('porcentaje_ingrediente_activo', 0)
            dosis = data.get('dosis', 0)
        else:
            # Default values for new entry
            area = ""
            producto = ""
            categoria = "Herbicida"
            tipo_aplicacion = "Pulverización"
            ingrediente_activo = ""
            porcentaje_ingrediente_activo = 0
            dosis = 0
        
        # Create form
        with st.form("proteccion_form"):
            st.subheader("Información General")
            col1, col2 = st.columns(2)
            
            with col1:
                area = st.text_input("Área Tratada", value=area)
                producto = st.text_input("Producto", value=producto)
            
            with col2:
                categoria = st.selectbox("Categoría", 
                                      options=["Herbicida", "Insecticida", "Fungicida", "Otro"],
                                      index=["Herbicida", "Insecticida", "Fungicida", "Otro"].index(categoria) if categoria in ["Herbicida", "Insecticida", "Fungicida", "Otro"] else 0)
                
                tipo_aplicacion = st.selectbox("Tipo de Aplicación", 
                                           options=["Pulverización", "Fumigación", "Aplicación dirigida", "Otro"],
                                           index=["Pulverización", "Fumigación", "Aplicación dirigida", "Otro"].index(tipo_aplicacion) if tipo_aplicacion in ["Pulverización", "Fumigación", "Aplicación dirigida", "Otro"] else 0)
            
            st.subheader("Detalles Técnicos")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                ingrediente_activo = st.text_input("Ingrediente Activo", value=ingrediente_activo)
            
            with col2:
                porcentaje_ingrediente_activo = st.number_input("Porcentaje del Ingrediente Activo (%)", 
                                                        min_value=0.0, max_value=100.0, step=0.1,
                                                        value=float(porcentaje_ingrediente_activo))
            
            with col3:
                dosis = st.number_input("Dosis (kg/ha o L/ha)", 
                                     min_value=0.0, step=0.1,
                                     value=float(dosis))
            
            submitted = st.form_submit_button("Revisar información antes de guardar")
            
            if submitted:
                # Validate input
                validation_errors = []
                
                if not validate_text(area, min_length=1):
                    validation_errors.append("El área tratada no puede estar vacía.")
                
                if not validate_text(producto, min_length=1):
                    validation_errors.append("El producto no puede estar vacío.")
                
                if not validate_text(ingrediente_activo, min_length=1):
                    validation_errors.append("El ingrediente activo no puede estar vacío.")
                
                if not validate_percentage(porcentaje_ingrediente_activo):
                    validation_errors.append("El porcentaje del ingrediente activo debe ser un valor entre 0 y 100.")
                
                if not validate_numeric(dosis, min_val=0):
                    validation_errors.append("La dosis debe ser un número positivo.")
                
                # If there are validation errors, display them and stop
                if validation_errors:
                    for error in validation_errors:
                        show_validation_error(error)
                    return
                
                # Store data temporarily in session state
                st.session_state.proteccion_temp_data = {
                    'uuid': st.session_state.proteccion_uuid,
                    'area': area,
                    'producto': producto,
                    'categoria': categoria,
                    'tipo_aplicacion': tipo_aplicacion,
                    'ingrediente_activo': ingrediente_activo,
                    'porcentaje_ingrediente_activo': porcentaje_ingrediente_activo,
                    'dosis': dosis
                }
                
                # Show summary for confirmation
                st.session_state.show_proteccion_summary = True
                
                # Rerun to show the summary
                st.rerun()
    
    # Show existing data if available
    if has_existing_data:
        st.subheader("Datos actuales de Protección de Cultivos")
        display_df = df.drop(columns=['uuid']) if 'uuid' in df.columns else df
        st.dataframe(display_df)
        
        # Allow deletion of entries
        if st.button("Eliminar Última Entrada"):
            if len(df) > 0:
                df = df.iloc[:-1]
                df.to_csv("data/proteccion_cultivos.csv", index=False)
                st.success("Última entrada eliminada. Recarga la página para ver los cambios.")
                st.rerun()