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
    
    # Create form
    with st.form("fertilizacion_form"):
        st.subheader("Detalles de Fertilización")
        col1, col2 = st.columns(2)
        
        with col1:
            area = st.selectbox("Área", options=["Pastura", "Verdeo", "Maíz", "Soja", "Otro"])
            hectareas = st.number_input("Hectáreas", min_value=0.0, format="%.2f")
            tipo = st.text_input("Tipo de Fertilizante")
            porcentaje_area = st.number_input("% del Área Total", min_value=0, max_value=100, value=100)
        
        with col2:
            cantidad_aplicada_kg_ha = st.number_input("Cantidad Aplicada (kg/ha)", min_value=0.0, format="%.2f")
            
            # Calculate total quantity
            cantidad_aplicada_total = cantidad_aplicada_kg_ha * hectareas * (porcentaje_area / 100)
            st.number_input("Cantidad Aplicada Total (kg)", 
                          min_value=0.0, 
                          value=cantidad_aplicada_total,
                          format="%.2f",
                          disabled=True)
            
            metodo_aplicacion = st.selectbox("Método de Aplicación", 
                                          options=["Incorporado", "Al voleo", "Otro"])
        
        st.subheader("Tecnologías de Aplicación")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            uso_inhibidores = st.selectbox("¿Usa Inhibidores?", options=["No", "Sí"])
        
        with col2:
            urea_protegida = st.selectbox("¿Usa Urea Protegida?", options=["No", "Sí"])
        
        with col3:
            ajuste_por_N = st.selectbox("¿Ajuste por N?", options=["No", "Sí"])
        
        submitted = st.form_submit_button("Guardar Información de Fertilización")
        
        if submitted:
            # Validate input
            validation_errors = []
            
            if not validate_numeric(hectareas, min_val=0):
                validation_errors.append("Las hectáreas deben ser un número positivo.")
            
            if not validate_text(tipo):
                validation_errors.append("El tipo de fertilizante es obligatorio.")
            
            if not validate_percentage(porcentaje_area):
                validation_errors.append("El porcentaje del área total debe ser un valor entre 0 y 100.")
            
            if not validate_numeric(cantidad_aplicada_kg_ha, min_val=0):
                validation_errors.append("La cantidad aplicada debe ser un número positivo.")
            
            # If there are validation errors, display them and stop
            if validation_errors:
                for error in validation_errors:
                    show_validation_error(error)
                return
            
            # Create data object
            data = {
                'uuid': st.session_state.fertilizacion_uuid,
                'área': area,
                'hectareas': hectareas,
                'tipo': tipo,
                '%_área_total': porcentaje_area,
                'cantidad_aplicada_kg_ha': cantidad_aplicada_kg_ha,
                'cantidad_aplicada_total': round(cantidad_aplicada_total, 2),
                'método_aplicación': metodo_aplicacion,
                'uso_inhibidores': uso_inhibidores,
                'urea_protegida': urea_protegida,
                'ajuste_por_N': ajuste_por_N
            }
            
            # Create dataframe
            new_df = pd.DataFrame([data])
            
            # Save dataframe
            save_dataframe(new_df, "fertilizacion.csv")
            
            # Generate new UUID for next entry
            st.session_state.fertilizacion_uuid = generate_uuid()
            
            # Show success message
            show_success_message("Datos guardados correctamente")
            
            # Clear form (hack: rerun the app)
            st.rerun()
    
    # Show existing data if available
    if has_existing_data:
        st.subheader("Datos actuales de Fertilización")
        display_df = df.drop(columns=['uuid']) if 'uuid' in df.columns else df
        st.dataframe(display_df)
        
        # Summary
        st.subheader("Resumen")
        total_fertilizante = df['cantidad_aplicada_total'].sum() if 'cantidad_aplicada_total' in df.columns else 0
        st.metric("Cantidad Total de Fertilizante Aplicado", f"{total_fertilizante:.2f} kg")
        
        # Allow deletion of entries
        if st.button("Eliminar Última Entrada"):
            if len(df) > 0:
                df = df.iloc[:-1]
                df.to_csv("data/fertilizacion.csv", index=False)
                st.success("Última entrada eliminada. Recarga la página para ver los cambios.")
                st.rerun()
