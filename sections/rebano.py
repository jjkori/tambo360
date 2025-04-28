import streamlit as st
import pandas as pd
from utils import save_dataframe, load_dataframe, validate_numeric, validate_text, generate_uuid, show_validation_error, show_success_message

def show_rebano():
    """Display and handle the Rebaño form"""
    st.title("Rebaño")
    
    # Check if we have existing data
    df = load_dataframe("rebano.csv")
    has_existing_data = not df.empty
    
    # Generate UUID if not present
    if "rebano_uuid" not in st.session_state:
        st.session_state.rebano_uuid = generate_uuid()
    
    # Create form
    with st.form("rebano_form"):
        st.subheader("Detalles de Categoría Animal")
        col1, col2 = st.columns(2)
        
        with col1:
            categorias = ["Guachera", "Recría", "Vaquillonas", "Vacas en Ordeñe", "Vacas Secas", "Toros", "Otro"]
            categoria = st.selectbox("Categoría", options=categorias)
            numero_animales = st.number_input("Número de Animales", min_value=0, step=1)
        
        with col2:
            peso_promedio = st.number_input("Peso Promedio (kg)", min_value=0.0, format="%.1f")
            horas_pastoreo = st.number_input("Horas de Pastoreo (horas/día)", min_value=0, max_value=24)
        
        dieta_materia_seca = st.number_input("Dieta Materia Seca (kg materia seca/animal/día)", 
                                          min_value=0.0, format="%.2f")
        
        # Optional: Add more detailed diet information
        st.subheader("Composición de la Dieta (opcional)")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            porcentaje_pastura = st.number_input("% Pastura", min_value=0, max_value=100, value=0)
        
        with col2:
            porcentaje_concentrado = st.number_input("% Concentrado", min_value=0, max_value=100, value=0)
        
        with col3:
            porcentaje_otros = st.number_input("% Otros", min_value=0, max_value=100, value=0)
        
        # Check if diet percentages sum to 100
        diet_sum = porcentaje_pastura + porcentaje_concentrado + porcentaje_otros
        if diet_sum > 0 and diet_sum != 100:
            st.warning(f"⚠️ La suma de los porcentajes de la dieta debe ser 100%. Actualmente: {diet_sum}%")
        
        submitted = st.form_submit_button("Guardar Información de Rebaño")
        
        if submitted:
            # Validate input
            validation_errors = []
            
            if not validate_numeric(numero_animales, min_val=0):
                validation_errors.append("El número de animales debe ser un número entero positivo.")
            
            if not validate_numeric(peso_promedio, min_val=0):
                validation_errors.append("El peso promedio debe ser un número positivo.")
            
            if not validate_numeric(horas_pastoreo, min_val=0, max_val=24):
                validation_errors.append("Las horas de pastoreo deben estar entre 0 y 24.")
            
            if not validate_numeric(dieta_materia_seca, min_val=0):
                validation_errors.append("La dieta de materia seca debe ser un número positivo.")
            
            if diet_sum > 0 and diet_sum != 100:
                validation_errors.append("Si ingresa composición de la dieta, la suma debe ser 100%.")
            
            # If there are validation errors, display them and stop
            if validation_errors:
                for error in validation_errors:
                    show_validation_error(error)
                return
            
            # Create data object
            data = {
                'uuid': st.session_state.rebano_uuid,
                'categoría': categoria,
                'número_animales': numero_animales,
                'peso_promedio': peso_promedio,
                'horas_pastoreo': horas_pastoreo,
                'dieta_materia_seca': dieta_materia_seca
            }
            
            # Add diet composition if provided
            if diet_sum > 0:
                data['porcentaje_pastura'] = porcentaje_pastura
                data['porcentaje_concentrado'] = porcentaje_concentrado
                data['porcentaje_otros'] = porcentaje_otros
            
            # Create dataframe
            new_df = pd.DataFrame([data])
            
            # Save dataframe
            save_dataframe(new_df, "rebano.csv")
            
            # Generate new UUID for next entry
            st.session_state.rebano_uuid = generate_uuid()
            
            # Show success message
            show_success_message("Datos guardados correctamente")
            
            # Clear form (hack: rerun the app)
            st.rerun()
    
    # Show existing data if available
    if has_existing_data:
        st.subheader("Datos actuales de Rebaño")
        display_df = df.drop(columns=['uuid']) if 'uuid' in df.columns else df
        st.dataframe(display_df)
        
        # Summary
        st.subheader("Resumen del Rebaño")
        total_animales = df['número_animales'].sum() if 'número_animales' in df.columns else 0
        
        # Calculate total weight
        if 'número_animales' in df.columns and 'peso_promedio' in df.columns:
            total_weight = sum(df['número_animales'] * df['peso_promedio'])
            average_weight = total_weight / total_animales if total_animales > 0 else 0
        else:
            total_weight = 0
            average_weight = 0
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Animales", f"{total_animales}")
        col2.metric("Peso Total Aproximado", f"{total_weight:.1f} kg")
        col3.metric("Peso Promedio", f"{average_weight:.1f} kg")
        
        # Allow deletion of entries
        if st.button("Eliminar Última Entrada"):
            if len(df) > 0:
                df = df.iloc[:-1]
                df.to_csv("data/rebano.csv", index=False)
                st.success("Última entrada eliminada. Recarga la página para ver los cambios.")
                st.rerun()
