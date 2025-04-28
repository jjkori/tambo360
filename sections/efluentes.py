import streamlit as st
import pandas as pd
from utils import save_dataframe, load_dataframe, validate_numeric, validate_percentage, validate_text, generate_uuid, show_validation_error, show_success_message

def show_efluentes():
    """Display and handle the Gestión de Efluentes form"""
    st.title("Gestión de Efluentes")
    
    # Check if we have existing data
    df = load_dataframe("efluentes.csv")
    has_existing_data = not df.empty
    
    # Generate UUID if not present
    if "efluentes_uuid" not in st.session_state:
        st.session_state.efluentes_uuid = generate_uuid()
    
    # Create form
    with st.form("efluentes_form"):
        st.subheader("Distribución de Efluentes por Sector")
        col1, col2 = st.columns(2)
        
        with col1:
            sectores = ["Ordeñe", "Corral", "Galpón", "Pastura", "Otro"]
            sector = st.selectbox("Sector", options=sectores)
            horas_dia = st.number_input("Horas por Día", min_value=0, max_value=24)
        
        with col2:
            manejos = [
                "Almacenaje sólidos", 
                "Laguna anaeróbica", 
                "Separación sólidos/líquidos",
                "Compostaje",
                "Aplicación directa",
                "Sin manejo"
            ]
            manejo_excretas = st.selectbox("Manejo de Excretas", options=manejos)
            eficiencia_separacion = st.number_input("Eficiencia de Separación (%)", 
                                              min_value=0, max_value=100, 
                                              value=0,
                                              disabled=manejo_excretas != "Separación sólidos/líquidos")
        
        # Optional: additional information
        st.subheader("Información Adicional")
        col1, col2 = st.columns(2)
        
        with col1:
            destino_liquidos = st.selectbox("Destino de Líquidos", 
                                         options=["Laguna", "Aplicación a campo", "Curso de agua", "Otro", "No aplicable"],
                                         disabled=manejo_excretas not in ["Laguna anaeróbica", "Separación sólidos/líquidos"])
        
        with col2:
            destino_solidos = st.selectbox("Destino de Sólidos", 
                                        options=["Compostaje", "Aplicación a campo", "Venta", "Otro", "No aplicable"],
                                        disabled=manejo_excretas not in ["Almacenaje sólidos", "Separación sólidos/líquidos", "Compostaje"])
        
        submitted = st.form_submit_button("Guardar Información de Gestión de Efluentes")
        
        if submitted:
            # Validate input
            validation_errors = []
            
            if not validate_numeric(horas_dia, min_val=0, max_val=24):
                validation_errors.append("Las horas por día deben estar entre 0 y 24.")
            
            if manejo_excretas == "Separación sólidos/líquidos" and not validate_percentage(eficiencia_separacion):
                validation_errors.append("La eficiencia de separación debe ser un porcentaje válido (0-100).")
            
            # If there are validation errors, display them and stop
            if validation_errors:
                for error in validation_errors:
                    show_validation_error(error)
                return
            
            # Create data object
            data = {
                'uuid': st.session_state.efluentes_uuid,
                'sector': sector,
                'horas_dia': horas_dia,
                'manejo_excretas': manejo_excretas,
                'eficiencia_separación': eficiencia_separacion if manejo_excretas == "Separación sólidos/líquidos" else None,
                'destino_liquidos': destino_liquidos if manejo_excretas in ["Laguna anaeróbica", "Separación sólidos/líquidos"] else "No aplicable",
                'destino_solidos': destino_solidos if manejo_excretas in ["Almacenaje sólidos", "Separación sólidos/líquidos", "Compostaje"] else "No aplicable"
            }
            
            # Create dataframe
            new_df = pd.DataFrame([data])
            
            # Save dataframe
            save_dataframe(new_df, "efluentes.csv")
            
            # Generate new UUID for next entry
            st.session_state.efluentes_uuid = generate_uuid()
            
            # Show success message
            show_success_message("Datos guardados correctamente")
            
            # Clear form (hack: rerun the app)
            st.rerun()
    
    # Show existing data if available
    if has_existing_data:
        st.subheader("Datos actuales de Gestión de Efluentes")
        display_df = df.drop(columns=['uuid']) if 'uuid' in df.columns else df
        st.dataframe(display_df)
        
        # Summary
        if 'sector' in df.columns and 'horas_dia' in df.columns:
            st.subheader("Resumen por Sector")
            sector_hours = df.groupby('sector')['horas_dia'].sum().reset_index()
            sector_hours.columns = ['Sector', 'Horas Totales por Día']
            st.dataframe(sector_hours)
        
        # Allow deletion of entries
        if st.button("Eliminar Última Entrada"):
            if len(df) > 0:
                df = df.iloc[:-1]
                df.to_csv("data/efluentes.csv", index=False)
                st.success("Última entrada eliminada. Recarga la página para ver los cambios.")
                st.rerun()
