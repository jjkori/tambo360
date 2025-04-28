
import streamlit as st
import pandas as pd
from datetime import datetime
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
        
        # Display confirmation summary
        st.markdown("### ✅ Resumen de Superficies e Insumos")
        
        # Create a formatted summary
        st.markdown(f"""
        ##### Información General
        * **Cultivo**: {data['cultivo']}
        * **Temporada de crecimiento**: {data['temporada']}
        * **Año de cosecha**: {data['anio_cosecha']}
        * **Hectáreas**: {data['hectareas']} ha
        * **Propósito del cultivo**: {data['proposito']}
        
        ##### Productividad y Residuos
        * **Productividad de Materia Verde**: {data['productividad_materia_verde']} kg/ha
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
        # Initialize form values from session state or defaults
        data = st.session_state.superficie_temp_data if st.session_state.superficie_temp_data else {
            'cultivo': '',
            'temporada': 'Verano',
            'hectareas': 0,
            'productividad_materia_verde': 0.0,
            'destino_residuos': 'Se deja distribuido en el campo',
            'anio_cosecha': datetime.now().year,
            'proposito': 'Pastoreo'
        }
        
        # Create form
        with st.form("superficie_form"):
            st.subheader("Información General")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                cultivos = [
                    "Maiz grano", "Silaje de maíz", "Silaje de sorgo", 
                    "Pastura de alfalfa", "Pastura base alfalfa", "Pasturas mezclas",
                    "Pastizal natural", "Moha – pastoreo", "Moha heno/silaje",
                    "Raigrás anual", "Avena", "Cebada forrajera", "Trigo forrajero",
                    "Centeno", "Triticale", "Vicia pastoreo", "Otro"
                ]
                cultivo = st.selectbox("Cultivo", options=cultivos)
                if cultivo == "Otro":
                    cultivo = st.text_input("Especificar otro cultivo")
            
            with col2:
                temporada = st.selectbox(
                    "Temporada de crecimiento",
                    options=["Verano", "Invierno", "Anual", "Perenne"]
                )
            
            with col3:
                anio_cosecha = st.number_input(
                    "Año de cosecha",
                    min_value=2000,
                    max_value=datetime.now().year + 1,
                    value=data['anio_cosecha'],
                    step=1
                )
            
            col1, col2 = st.columns(2)
            
            with col1:
                hectareas = st.number_input(
                    "Hectáreas",
                    min_value=0,
                    step=1,
                    value=int(data['hectareas'])
                )
            
            with col2:
                proposito = st.selectbox(
                    "Propósito del cultivo",
                    options=["Pastoreo", "Silaje", "Henolaje", "Otro forraje conservado"]
                )
            
            st.subheader("Productividad y Residuos")
            productividad_materia_verde = st.number_input(
                "Productividad de Materia Verde (kg/ha)",
                min_value=0.0,
                step=100.0,
                value=float(data['productividad_materia_verde'])
            )
            
            destino_residuos = st.selectbox(
                "Destino de Residuos",
                options=[
                    "Retirada del campo para su uso o venta",
                    "Quemado en el campo",
                    "Se deja distribuido en el campo",
                    "Incorporado",
                    "Acolchado",
                    "Retirada; compost de aireación forzada",
                    "Retirada; compost sin aireación forzada",
                    "Eliminado; Se deja sin tratar en montones o fosas"
                ]
            )
            
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
                    'anio_cosecha': anio_cosecha,
                    'hectareas': hectareas,
                    'proposito': proposito,
                    'productividad_materia_verde': productividad_materia_verde,
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
