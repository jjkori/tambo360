import streamlit as st
import pandas as pd
from utils import save_dataframe, load_dataframe, validate_numeric, generate_uuid, show_validation_error, show_success_message

def show_energia():
    """Display and handle the Energía form"""
    st.title("Energía")
    
    # Check if we have existing data
    df = load_dataframe("energia.csv")
    has_existing_data = not df.empty
    
    # Generate UUID if not present
    if "energia_uuid" not in st.session_state:
        st.session_state.energia_uuid = generate_uuid()
    
    # Create form
    with st.form("energia_form"):
        st.subheader("Consumo Energético Anual")
        col1, col2 = st.columns(2)
        
        with col1:
            consumo_diesel = st.number_input("Consumo Diesel (L/año)", min_value=0)
            consumo_gasolina = st.number_input("Consumo Gasolina (L/año)", min_value=0)
        
        with col2:
            consumo_GNC = st.number_input("Consumo GNC (m³/año)", min_value=0)
            consumo_electricidad = st.number_input("Consumo Electricidad (kWh/año)", min_value=0)
        
        # Optional: Add renewable energy sources
        st.subheader("Fuentes de Energía Renovable (opcional)")
        col1, col2 = st.columns(2)
        
        with col1:
            uso_paneles_solares = st.selectbox("¿Utiliza Paneles Solares?", options=["No", "Sí"])
            if uso_paneles_solares == "Sí":
                capacidad_paneles = st.number_input("Capacidad Instalada (kW)", min_value=0.0, format="%.2f")
            else:
                capacidad_paneles = 0
        
        with col2:
            uso_biodigestores = st.selectbox("¿Utiliza Biodigestores?", options=["No", "Sí"])
            if uso_biodigestores == "Sí":
                capacidad_biodigestores = st.number_input("Capacidad (m³)", min_value=0.0, format="%.2f")
            else:
                capacidad_biodigestores = 0
        
        submitted = st.form_submit_button("Guardar Información de Energía")
        
        if submitted:
            # Validate input
            validation_errors = []
            
            if not validate_numeric(consumo_diesel, min_val=0):
                validation_errors.append("El consumo de diesel debe ser un número positivo.")
            
            if not validate_numeric(consumo_gasolina, min_val=0):
                validation_errors.append("El consumo de gasolina debe ser un número positivo.")
            
            if not validate_numeric(consumo_GNC, min_val=0):
                validation_errors.append("El consumo de GNC debe ser un número positivo.")
            
            if not validate_numeric(consumo_electricidad, min_val=0):
                validation_errors.append("El consumo de electricidad debe ser un número positivo.")
            
            if uso_paneles_solares == "Sí" and not validate_numeric(capacidad_paneles, min_val=0):
                validation_errors.append("La capacidad de paneles solares debe ser un número positivo.")
            
            if uso_biodigestores == "Sí" and not validate_numeric(capacidad_biodigestores, min_val=0):
                validation_errors.append("La capacidad de biodigestores debe ser un número positivo.")
            
            # If there are validation errors, display them and stop
            if validation_errors:
                for error in validation_errors:
                    show_validation_error(error)
                return
            
            # Create data object
            data = {
                'uuid': st.session_state.energia_uuid,
                'consumo_diesel': consumo_diesel,
                'consumo_gasolina': consumo_gasolina,
                'consumo_GNC': consumo_GNC,
                'consumo_electricidad': consumo_electricidad,
                'uso_paneles_solares': uso_paneles_solares,
                'capacidad_paneles': capacidad_paneles if uso_paneles_solares == "Sí" else 0,
                'uso_biodigestores': uso_biodigestores,
                'capacidad_biodigestores': capacidad_biodigestores if uso_biodigestores == "Sí" else 0
            }
            
            # Create dataframe
            new_df = pd.DataFrame([data])
            
            # Save dataframe
            save_dataframe(new_df, "energia.csv")
            
            # Generate new UUID for next entry
            st.session_state.energia_uuid = generate_uuid()
            
            # Show success message
            show_success_message("Datos guardados correctamente")
    
    # Show existing data if available
    if has_existing_data:
        st.subheader("Datos actuales de Energía")
        display_df = df.drop(columns=['uuid']) if 'uuid' in df.columns else df
        st.dataframe(display_df)
        
        # Calculate approximate CO2 equivalent emissions
        st.subheader("Estimación de Emisiones CO2 Equivalente")
        
        # Conversion factors (approximate)
        diesel_co2_factor = 2.68  # kg CO2 per L
        gasolina_co2_factor = 2.31  # kg CO2 per L
        gnc_co2_factor = 1.86  # kg CO2 per m³
        electricity_co2_factor = 0.38  # kg CO2 per kWh (varies by country)
        
        latest_data = df.iloc[-1]
        
        diesel_co2 = latest_data['consumo_diesel'] * diesel_co2_factor if 'consumo_diesel' in latest_data else 0
        gasolina_co2 = latest_data['consumo_gasolina'] * gasolina_co2_factor if 'consumo_gasolina' in latest_data else 0
        gnc_co2 = latest_data['consumo_GNC'] * gnc_co2_factor if 'consumo_GNC' in latest_data else 0
        electricity_co2 = latest_data['consumo_electricidad'] * electricity_co2_factor if 'consumo_electricidad' in latest_data else 0
        
        total_co2 = diesel_co2 + gasolina_co2 + gnc_co2 + electricity_co2
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Diesel", f"{diesel_co2:.2f} kg CO2")
        col2.metric("Gasolina", f"{gasolina_co2:.2f} kg CO2")
        col3.metric("GNC", f"{gnc_co2:.2f} kg CO2")
        col4.metric("Electricidad", f"{electricity_co2:.2f} kg CO2")
        
        st.metric("Total Emisiones CO2 Equivalente", f"{total_co2:.2f} kg CO2")
        
        # Allow deletion of entries
        if st.button("Eliminar Última Entrada"):
            if len(df) > 0:
                df = df.iloc[:-1]
                df.to_csv("data/energia.csv", index=False)
                st.success("Última entrada eliminada. Recarga la página para ver los cambios.")
                st.rerun()
