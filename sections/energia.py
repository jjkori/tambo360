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
    
    # Track form submission state
    if "show_energia_summary" not in st.session_state:
        st.session_state.show_energia_summary = False
    
    # Store form data temporarily
    if "energia_temp_data" not in st.session_state:
        st.session_state.energia_temp_data = {}
    
    # Handle confirmation
    if st.session_state.show_energia_summary:
        # Get the temporary data
        data = st.session_state.energia_temp_data
        
        # Display confirmation summary in a nice format with green checkmark
        st.markdown("### ✅ Resumen de Energía")
        
        # Calculate CO2 emissions
        diesel_co2_factor = 2.68  # kg CO2 per L
        gasolina_co2_factor = 2.31  # kg CO2 per L
        gnc_co2_factor = 1.86  # kg CO2 per m³
        electricity_co2_factor = 0.38  # kg CO2 per kWh
        
        diesel_co2 = data['consumo_diesel'] * diesel_co2_factor
        gasolina_co2 = data['consumo_gasolina'] * gasolina_co2_factor
        gnc_co2 = data['consumo_GNC'] * gnc_co2_factor
        electricity_co2 = data['consumo_electricidad'] * electricity_co2_factor
        total_co2 = diesel_co2 + gasolina_co2 + gnc_co2 + electricity_co2
        
        # Create a formatted summary
        st.markdown(f"""
        ##### Consumo Energético Anual
        * **Consumo Diesel**: {data['consumo_diesel']} L/año
        * **Consumo Gasolina**: {data['consumo_gasolina']} L/año
        * **Consumo GNC**: {data['consumo_GNC']} m³/año
        * **Consumo Electricidad**: {data['consumo_electricidad']} kWh/año
        
        ##### Emisiones CO2 Estimadas
        * **Diesel**: {diesel_co2:.2f} kg CO2
        * **Gasolina**: {gasolina_co2:.2f} kg CO2
        * **GNC**: {gnc_co2:.2f} kg CO2
        * **Electricidad**: {electricity_co2:.2f} kg CO2
        * **Total Emisiones**: {total_co2:.2f} kg CO2
        """)
        
        # Show renewable energy if used
        if data['uso_paneles_solares'] == "Sí" or data['uso_biodigestores'] == "Sí":
            st.markdown("##### Fuentes de Energía Renovable")
            
            if data['uso_paneles_solares'] == "Sí":
                st.markdown(f"* **Paneles Solares**: {data['capacidad_paneles']:.2f} kW de capacidad instalada")
            
            if data['uso_biodigestores'] == "Sí":
                st.markdown(f"* **Biodigestores**: {data['capacidad_biodigestores']:.2f} m³ de capacidad")
        
        # Add confirmation button
        if st.button("📝 Confirmar y guardar", key="confirm_energia", type="primary"):
            # Create dataframe
            new_df = pd.DataFrame([data])
            
            # Save dataframe
            save_dataframe(new_df, "energia.csv")
            
            # Generate new UUID for next entry
            st.session_state.energia_uuid = generate_uuid()
            
            # Reset the summary view
            st.session_state.show_energia_summary = False
            st.session_state.energia_temp_data = {}
            
            # Show success message
            show_success_message("Datos guardados correctamente")
            
            # Rerun to refresh the app
            st.rerun()
        
        # Add back button
        if st.button("↩ Volver y editar", key="back_energia"):
            st.session_state.show_energia_summary = False
            st.rerun()
            
        # Add divider
        st.divider()
        
    # Only show the form if we're not in summary mode
    if not st.session_state.show_energia_summary:
        # Initialize form values
        if has_existing_data and not st.session_state.energia_temp_data:
            # Get the most recent entry
            latest_data = df.iloc[-1]
            
            # Pre-fill form fields
            consumo_diesel = latest_data.get('consumo_diesel', 0)
            consumo_gasolina = latest_data.get('consumo_gasolina', 0)
            consumo_GNC = latest_data.get('consumo_GNC', 0)
            consumo_electricidad = latest_data.get('consumo_electricidad', 0)
            uso_paneles_solares = latest_data.get('uso_paneles_solares', "No")
            capacidad_paneles = latest_data.get('capacidad_paneles', 0)
            uso_biodigestores = latest_data.get('uso_biodigestores', "No")
            capacidad_biodigestores = latest_data.get('capacidad_biodigestores', 0)
        elif st.session_state.energia_temp_data:
            # Get data from session state if we're coming back from summary
            data = st.session_state.energia_temp_data
            consumo_diesel = data.get('consumo_diesel', 0)
            consumo_gasolina = data.get('consumo_gasolina', 0)
            consumo_GNC = data.get('consumo_GNC', 0)
            consumo_electricidad = data.get('consumo_electricidad', 0)
            uso_paneles_solares = data.get('uso_paneles_solares', "No")
            capacidad_paneles = data.get('capacidad_paneles', 0)
            uso_biodigestores = data.get('uso_biodigestores', "No")
            capacidad_biodigestores = data.get('capacidad_biodigestores', 0)
        else:
            # Default values for new entry
            consumo_diesel = 0
            consumo_gasolina = 0
            consumo_GNC = 0
            consumo_electricidad = 0
            uso_paneles_solares = "No"
            capacidad_paneles = 0
            uso_biodigestores = "No"
            capacidad_biodigestores = 0
        
        # Create form
        with st.form("energia_form"):
            st.subheader("Consumo Energético Anual")
            col1, col2 = st.columns(2)
            
            with col1:
                consumo_diesel = st.number_input("Consumo Diesel (L/año)", min_value=0, value=consumo_diesel)
                consumo_gasolina = st.number_input("Consumo Gasolina (L/año)", min_value=0, value=consumo_gasolina)
            
            with col2:
                consumo_GNC = st.number_input("Consumo GNC (m³/año)", min_value=0, value=consumo_GNC)
                consumo_electricidad = st.number_input("Consumo Electricidad (kWh/año)", min_value=0, value=consumo_electricidad)
            
            # Optional: Add renewable energy sources
            st.subheader("Fuentes de Energía Renovable (opcional)")
            col1, col2 = st.columns(2)
            
            with col1:
                uso_paneles_solares = st.selectbox("¿Utiliza Paneles Solares?", options=["No", "Sí"], index=0 if uso_paneles_solares == "No" else 1)
                if uso_paneles_solares == "Sí":
                    capacidad_paneles = st.number_input("Capacidad Instalada (kW)", min_value=0.0, format="%.2f", value=float(capacidad_paneles))
                else:
                    capacidad_paneles = 0
            
            with col2:
                uso_biodigestores = st.selectbox("¿Utiliza Biodigestores?", options=["No", "Sí"], index=0 if uso_biodigestores == "No" else 1)
                if uso_biodigestores == "Sí":
                    capacidad_biodigestores = st.number_input("Capacidad (m³)", min_value=0.0, format="%.2f", value=float(capacidad_biodigestores))
                else:
                    capacidad_biodigestores = 0
            
            submitted = st.form_submit_button("Revisar información antes de guardar")
            
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
                
                # Store data temporarily in session state
                st.session_state.energia_temp_data = {
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
                
                # Show summary for confirmation
                st.session_state.show_energia_summary = True
                
                # Rerun to show the summary
                st.rerun()
    
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