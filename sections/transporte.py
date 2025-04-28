import streamlit as st
import pandas as pd
from utils import save_dataframe, load_dataframe, validate_numeric, validate_text, generate_uuid, show_validation_error, show_success_message

def show_transporte():
    """Display and handle the Transporte form"""
    st.title("Transporte")
    
    # Check if we have existing data
    df = load_dataframe("transporte.csv")
    has_existing_data = not df.empty
    
    # Generate UUID if not present
    if "transporte_uuid" not in st.session_state:
        st.session_state.transporte_uuid = generate_uuid()
    
    # Create form
    with st.form("transporte_form"):
        st.subheader("Detalles de Transporte")
        col1, col2 = st.columns(2)
        
        with col1:
            producto_transportado = st.text_input("Producto Transportado")
            inicio = st.text_input("Punto de Inicio")
        
        with col2:
            destino = st.text_input("Punto de Destino")
            distancia_km = st.number_input("Distancia (km)", min_value=0.0, format="%.1f")
        
        # Optional: additional information
        st.subheader("Información Adicional (opcional)")
        col1, col2 = st.columns(2)
        
        with col1:
            tipo_vehiculo = st.selectbox("Tipo de Vehículo", 
                                      options=["Camión", "Camioneta", "Tractor", "Otro"])
            frecuencia = st.selectbox("Frecuencia", 
                                   options=["Diario", "Semanal", "Mensual", "Anual", "Ocasional"])
        
        with col2:
            tipo_combustible = st.selectbox("Tipo de Combustible", 
                                         options=["Diesel", "Gasolina", "GNC", "Otro"])
            carga_promedio = st.number_input("Carga Promedio (kg)", min_value=0)
        
        submitted = st.form_submit_button("Guardar Información de Transporte")
        
        if submitted:
            # Validate input
            validation_errors = []
            
            if not validate_text(producto_transportado):
                validation_errors.append("El producto transportado es obligatorio.")
            
            if not validate_text(inicio):
                validation_errors.append("El punto de inicio es obligatorio.")
            
            if not validate_text(destino):
                validation_errors.append("El punto de destino es obligatorio.")
            
            if not validate_numeric(distancia_km, min_val=0):
                validation_errors.append("La distancia debe ser un número positivo.")
            
            # If there are validation errors, display them and stop
            if validation_errors:
                for error in validation_errors:
                    show_validation_error(error)
                return
            
            # Create data object
            data = {
                'uuid': st.session_state.transporte_uuid,
                'producto_transportado': producto_transportado,
                'inicio': inicio,
                'destino': destino,
                'distancia_km': distancia_km,
                'tipo_vehiculo': tipo_vehiculo,
                'frecuencia': frecuencia,
                'tipo_combustible': tipo_combustible,
                'carga_promedio': carga_promedio
            }
            
            # Create dataframe
            new_df = pd.DataFrame([data])
            
            # Save dataframe
            save_dataframe(new_df, "transporte.csv")
            
            # Generate new UUID for next entry
            st.session_state.transporte_uuid = generate_uuid()
            
            # Show success message
            show_success_message("Datos guardados correctamente")
            
            # Clear form (hack: rerun the app)
            st.rerun()
    
    # Show existing data if available
    if has_existing_data:
        st.subheader("Datos actuales de Transporte")
        display_df = df.drop(columns=['uuid']) if 'uuid' in df.columns else df
        st.dataframe(display_df)
        
        # Summary
        st.subheader("Resumen")
        total_distancia = df['distancia_km'].sum() if 'distancia_km' in df.columns else 0
        st.metric("Distancia Total", f"{total_distancia:.1f} km")
        
        # Allow deletion of entries
        if st.button("Eliminar Última Entrada"):
            if len(df) > 0:
                df = df.iloc[:-1]
                df.to_csv("data/transporte.csv", index=False)
                st.success("Última entrada eliminada. Recarga la página para ver los cambios.")
                st.rerun()
