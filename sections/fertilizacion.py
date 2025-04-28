import streamlit as st
import pandas as pd
from utils import save_dataframe, load_dataframe, validate_numeric, validate_percentage, validate_text, generate_uuid, show_validation_error, show_success_message

def show_fertilizacion():
    """Display and handle the Fertilización form"""
    st.title("Fertilización")
    
    # Check if we have existing data
    df = load_dataframe("fertilizacion.csv")
    has_existing_data = not df.empty
    
    # Generate UUID if not present
    if "fertilizacion_uuid" not in st.session_state:
        st.session_state.fertilizacion_uuid = generate_uuid()
    
    # Track form submission state
    if "show_fertilizacion_summary" not in st.session_state:
        st.session_state.show_fertilizacion_summary = False
    
    # Store form data temporarily
    if "fertilizacion_temp_data" not in st.session_state:
        st.session_state.fertilizacion_temp_data = {}
    
    # Handle confirmation
    if st.session_state.show_fertilizacion_summary:
        # Get the temporary data
        data = st.session_state.fertilizacion_temp_data
        
        # Display confirmation summary in a nice format with green checkmark
        st.markdown("### ✅ Resumen de Fertilización")
        
        # Create a formatted summary
        st.markdown(f"""
        ##### Información General
        * **Área Fertilizada**: {data['area']}
        * **Hectáreas**: {data['hectareas']} ha
        * **Tipo de Fertilizante**: {data['tipo']}
        * **Porcentaje del Área**: {data['porcentaje_area']}%
        
        ##### Aplicación
        * **Cantidad Aplicada por Hectárea**: {data['cantidad_aplicada_kg_ha']} kg/ha
        * **Cantidad Total Aplicada**: {data['cantidad_aplicada_total']} kg
        * **Método de Aplicación**: {data['metodo_aplicacion']}
        
        ##### Técnicas y Ajustes
        * **Uso de Inhibidores**: {data['uso_inhibidores']}
        * **Urea Protegida**: {data['urea_protegida']}
        * **Ajuste de N**: {data['ajuste_n']}
        """)
        
        # Add confirmation button
        if st.button("📝 Confirmar y guardar", key="confirm_fertilizacion", type="primary"):
            # Create dataframe
            new_df = pd.DataFrame([data])
            
            # Save dataframe
            save_dataframe(new_df, "fertilizacion.csv")
            
            # Generate new UUID for next entry
            st.session_state.fertilizacion_uuid = generate_uuid()
            
            # Reset the summary view
            st.session_state.show_fertilizacion_summary = False
            st.session_state.fertilizacion_temp_data = {}
            
            # Show success message
            show_success_message("Datos guardados correctamente")
            
            # Rerun to refresh the app
            st.rerun()
        
        # Add back button
        if st.button("↩ Volver y editar", key="back_fertilizacion"):
            st.session_state.show_fertilizacion_summary = False
            st.rerun()
            
        # Add divider
        st.divider()
    
    # Only show the form if we're not in summary mode
    if not st.session_state.show_fertilizacion_summary:
        # Initialize form values
        if has_existing_data and not st.session_state.fertilizacion_temp_data:
            # Get the most recent entry
            latest_data = df.iloc[-1]
            
            # Pre-fill form fields
            area = latest_data.get('area', "")
            hectareas = latest_data.get('hectareas', 0.0)
            tipo = latest_data.get('tipo', "Urea")
            porcentaje_area = latest_data.get('porcentaje_area', 0)
            cantidad_aplicada_kg_ha = latest_data.get('cantidad_aplicada_kg_ha', 0.0)
            cantidad_aplicada_total = latest_data.get('cantidad_aplicada_total', 0.0)
            metodo_aplicacion = latest_data.get('metodo_aplicacion', "Voleo")
            uso_inhibidores = latest_data.get('uso_inhibidores', "No")
            urea_protegida = latest_data.get('urea_protegida', "No")
            ajuste_n = latest_data.get('ajuste_n', "No")
        elif st.session_state.fertilizacion_temp_data:
            # Get data from session state if we're coming back from summary
            data = st.session_state.fertilizacion_temp_data
            area = data.get('area', "")
            hectareas = data.get('hectareas', 0.0)
            tipo = data.get('tipo', "Urea")
            porcentaje_area = data.get('porcentaje_area', 0)
            cantidad_aplicada_kg_ha = data.get('cantidad_aplicada_kg_ha', 0.0)
            cantidad_aplicada_total = data.get('cantidad_aplicada_total', 0.0)
            metodo_aplicacion = data.get('metodo_aplicacion', "Voleo")
            uso_inhibidores = data.get('uso_inhibidores', "No")
            urea_protegida = data.get('urea_protegida', "No")
            ajuste_n = data.get('ajuste_n', "No")
        else:
            # Default values for new entry
            area = ""
            hectareas = 0.0
            tipo = "Urea"
            porcentaje_area = 0
            cantidad_aplicada_kg_ha = 0.0
            cantidad_aplicada_total = 0.0
            metodo_aplicacion = "Voleo"
            uso_inhibidores = "No"
            urea_protegida = "No"
            ajuste_n = "No"
        
        # Create form
        with st.form("fertilizacion_form"):
            st.subheader("Información General")
            col1, col2 = st.columns(2)
            
            with col1:
                area = st.text_input("Área Fertilizada", value=area)
                hectareas = st.number_input("Hectáreas", min_value=0.0, step=0.1, value=float(hectareas))
            
            with col2:
                tipo = st.selectbox("Tipo de Fertilizante", 
                                 options=["Urea", "Fosfato diamónico", "Nitrato de amonio", "NPK", "Orgánico", "Otro"],
                                 index=["Urea", "Fosfato diamónico", "Nitrato de amonio", "NPK", "Orgánico", "Otro"].index(tipo) if tipo in ["Urea", "Fosfato diamónico", "Nitrato de amonio", "NPK", "Orgánico", "Otro"] else 0)
                
                porcentaje_area = st.number_input("Porcentaje del Área (%)", min_value=0, max_value=100, value=porcentaje_area)
            
            st.subheader("Aplicación")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                cantidad_aplicada_kg_ha = st.number_input("Cantidad Aplicada (kg/ha)", 
                                                    min_value=0.0, step=0.1,
                                                    value=float(cantidad_aplicada_kg_ha))
            
            with col2:
                cantidad_aplicada_total = st.number_input("Cantidad Total Aplicada (kg)", 
                                                   min_value=0.0, step=0.1,
                                                   value=float(cantidad_aplicada_total))
            
            with col3:
                metodo_aplicacion = st.selectbox("Método de Aplicación", 
                                              options=["Voleo", "Localizado", "Fertirrigación", "Otro"],
                                              index=["Voleo", "Localizado", "Fertirrigación", "Otro"].index(metodo_aplicacion) if metodo_aplicacion in ["Voleo", "Localizado", "Fertirrigación", "Otro"] else 0)
            
            st.subheader("Técnicas y Ajustes")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                uso_inhibidores = st.selectbox("¿Usa Inhibidores?", 
                                           options=["No", "Sí"],
                                           index=0 if uso_inhibidores == "No" else 1)
            
            with col2:
                urea_protegida = st.selectbox("¿Usa Urea Protegida?", 
                                          options=["No", "Sí"],
                                          index=0 if urea_protegida == "No" else 1)
            
            with col3:
                ajuste_n = st.selectbox("¿Realiza Ajuste de N?", 
                                     options=["No", "Sí"],
                                     index=0 if ajuste_n == "No" else 1)
            
            submitted = st.form_submit_button("Revisar información antes de guardar")
            
            if submitted:
                # Validate input
                validation_errors = []
                
                if not validate_text(area, min_length=1):
                    validation_errors.append("El área fertilizada no puede estar vacía.")
                
                if not validate_numeric(hectareas, min_val=0):
                    validation_errors.append("Las hectáreas deben ser un número positivo.")
                
                if not validate_percentage(porcentaje_area):
                    validation_errors.append("El porcentaje del área debe ser un valor entre 0 y 100.")
                
                if not validate_numeric(cantidad_aplicada_kg_ha, min_val=0):
                    validation_errors.append("La cantidad aplicada por hectárea debe ser un número positivo.")
                
                if not validate_numeric(cantidad_aplicada_total, min_val=0):
                    validation_errors.append("La cantidad total aplicada debe ser un número positivo.")
                
                # If there are validation errors, display them and stop
                if validation_errors:
                    for error in validation_errors:
                        show_validation_error(error)
                    return
                
                # Store data temporarily in session state
                st.session_state.fertilizacion_temp_data = {
                    'uuid': st.session_state.fertilizacion_uuid,
                    'area': area,
                    'hectareas': hectareas,
                    'tipo': tipo,
                    'porcentaje_area': porcentaje_area,
                    'cantidad_aplicada_kg_ha': cantidad_aplicada_kg_ha,
                    'cantidad_aplicada_total': cantidad_aplicada_total,
                    'metodo_aplicacion': metodo_aplicacion,
                    'uso_inhibidores': uso_inhibidores,
                    'urea_protegida': urea_protegida,
                    'ajuste_n': ajuste_n
                }
                
                # Show summary for confirmation
                st.session_state.show_fertilizacion_summary = True
                
                # Rerun to show the summary
                st.rerun()
    
    # Show existing data if available
    if has_existing_data:
        st.subheader("Datos actuales de Fertilización")
        display_df = df.drop(columns=['uuid']) if 'uuid' in df.columns else df
        st.dataframe(display_df)
        
        # Allow deletion of entries
        if st.button("Eliminar Última Entrada"):
            if len(df) > 0:
                df = df.iloc[:-1]
                df.to_csv("data/fertilizacion.csv", index=False)
                st.success("Última entrada eliminada. Recarga la página para ver los cambios.")
                st.rerun()