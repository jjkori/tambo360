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
    
    # Create form
    with st.form("proteccion_cultivos_form"):
        st.subheader("Detalles de Aplicación")
        col1, col2 = st.columns(2)
        
        with col1:
            area = st.text_input("Área/Cultivo")
            producto = st.text_input("Nombre del Producto")
            categoria = st.selectbox("Categoría", 
                                 options=["Herbicida", "Insecticida", "Fungicida", "Otro"])
        
        with col2:
            tipo_aplicacion = st.selectbox("Tipo de Aplicación", 
                                       options=["Preemergente", "Postemergente", "No Aplicable"])
            porcentaje_ingrediente_activo = st.number_input("% Ingrediente Activo", 
                                                        min_value=0.0, max_value=100.0, 
                                                        format="%.2f")
            dosis = st.number_input("Dosis (kg o L por ha)", min_value=0.0, format="%.3f")
        
        ingrediente_activo = st.text_input("Ingrediente Activo")
        
        submitted = st.form_submit_button("Guardar Información de Protección de Cultivos")
        
        if submitted:
            # Validate input
            validation_errors = []
            
            if not validate_text(area):
                validation_errors.append("El área/cultivo es obligatorio.")
            
            if not validate_text(producto):
                validation_errors.append("El nombre del producto es obligatorio.")
            
            if not validate_percentage(porcentaje_ingrediente_activo):
                validation_errors.append("El porcentaje de ingrediente activo debe ser un valor entre 0 y 100.")
            
            if not validate_numeric(dosis, min_val=0):
                validation_errors.append("La dosis debe ser un número positivo.")
            
            if not validate_text(ingrediente_activo):
                validation_errors.append("El ingrediente activo es obligatorio.")
            
            # If there are validation errors, display them and stop
            if validation_errors:
                for error in validation_errors:
                    show_validation_error(error)
                return
            
            # Create data object
            data = {
                'uuid': st.session_state.proteccion_uuid,
                'área': area,
                'producto': producto,
                'categoría': categoria.lower(),  # Store in lowercase for consistency
                'tipo_aplicacion': tipo_aplicacion,
                '%_ingrediente_activo': porcentaje_ingrediente_activo,
                'dosis': dosis,
                'ingrediente_activo': ingrediente_activo
            }
            
            # Create dataframe
            new_df = pd.DataFrame([data])
            
            # Save dataframe
            save_dataframe(new_df, "proteccion_cultivos.csv")
            
            # Generate new UUID for next entry
            st.session_state.proteccion_uuid = generate_uuid()
            
            # Show success message
            show_success_message("Datos guardados correctamente")
            
            # Clear form (hack: rerun the app)
            st.rerun()
    
    # Show existing data if available
    if has_existing_data:
        st.subheader("Datos actuales de Protección de Cultivos")
        display_df = df.drop(columns=['uuid']) if 'uuid' in df.columns else df
        st.dataframe(display_df)
        
        # Summary by category
        if 'categoría' in df.columns:
            st.subheader("Resumen por Categoría")
            category_counts = df['categoría'].value_counts().reset_index()
            category_counts.columns = ['Categoría', 'Cantidad de Productos']
            st.dataframe(category_counts)
        
        # Allow deletion of entries
        if st.button("Eliminar Última Entrada"):
            if len(df) > 0:
                df = df.iloc[:-1]
                df.to_csv("data/proteccion_cultivos.csv", index=False)
                st.success("Última entrada eliminada. Recarga la página para ver los cambios.")
                st.rerun()
