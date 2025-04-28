import streamlit as st
import pandas as pd
from utils import save_dataframe, load_dataframe, validate_numeric, validate_percentage, validate_text, generate_uuid, show_validation_error, show_success_message

def show_datos_generales():
    """Display and handle the Datos Generales form"""
    st.title("Datos Generales del Tambo")
    
    # Check if we have existing data
    datos_df = load_dataframe("datos_generales.csv")
    has_existing_data = not datos_df.empty
    
    # Generate UUID if not present
    if "datos_uuid" not in st.session_state:
        st.session_state.datos_uuid = generate_uuid()
    
    # Initialize form with existing data if available
    if has_existing_data:
        # Get the most recent entry
        latest_data = datos_df.iloc[-1]
        
        # Pre-fill form fields if they exist in the dataframe
        nombre_tambo = latest_data.get('nombre_tambo', "") if 'nombre_tambo' in latest_data else ""
        ciudad = latest_data.get('ciudad', "") if 'ciudad' in latest_data else ""
        raza = latest_data.get('raza', "Holstein") if 'raza' in latest_data else "Holstein"
        año = latest_data.get('año', 2023) if 'año' in latest_data else 2023
        mes = latest_data.get('mes', "Enero") if 'mes' in latest_data else "Enero"
        sup_total = latest_data.get('sup_total', "") if 'sup_total' in latest_data else ""
        sup_vt = latest_data.get('sup_vt', "") if 'sup_vt' in latest_data else ""
        produccion_ind = latest_data.get('produccion_ind', "") if 'produccion_ind' in latest_data else ""
        vacas_ordeñe = latest_data.get('vacas_ordeñe', "") if 'vacas_ordeñe' in latest_data else ""
        venta_industria = latest_data.get('venta_industria', 100) if 'venta_industria' in latest_data else 100
        uso_queseria = latest_data.get('uso_queseria', 0) if 'uso_queseria' in latest_data else 0
        descarte = latest_data.get('descarte', 0) if 'descarte' in latest_data else 0
        porcentaje_proteina = latest_data.get('porcentaje_proteina', "") if 'porcentaje_proteina' in latest_data else ""
        porcentaje_grasa = latest_data.get('porcentaje_grasa', "") if 'porcentaje_grasa' in latest_data else ""
    else:
        # Default values for new entry
        nombre_tambo = ""
        ciudad = ""
        raza = "Holstein"
        año = 2023
        mes = "Enero"
        sup_total = ""
        sup_vt = ""
        produccion_ind = ""
        vacas_ordeñe = ""
        venta_industria = 100
        uso_queseria = 0
        descarte = 0
        porcentaje_proteina = ""
        porcentaje_grasa = ""
    
    # Create form
    with st.form("datos_generales_form"):
        st.subheader("Información General")
        col1, col2 = st.columns(2)
        
        with col1:
            nombre_tambo = st.text_input("Nombre del Tambo", value=nombre_tambo)
            ciudad = st.text_input("Ciudad/Localidad", value=ciudad)
            raza = st.selectbox("Raza predominante", 
                               options=["Holstein", "Jersey", "Cruza", "Otro"],
                               index=["Holstein", "Jersey", "Cruza", "Otro"].index(raza) if raza in ["Holstein", "Jersey", "Cruza", "Otro"] else 0)
            
            st.subheader("Ubicación GPS")
            latitud = st.number_input("Latitud", 
                                    min_value=-90.0, 
                                    max_value=90.0, 
                                    value=float(latest_data.get('latitud', 0)) if has_existing_data else 0.0,
                                    format="%.6f",
                                    help="Ingrese la latitud en grados decimales")
            longitud = st.number_input("Longitud", 
                                     min_value=-180.0, 
                                     max_value=180.0, 
                                     value=float(latest_data.get('longitud', 0)) if has_existing_data else 0.0,
                                     format="%.6f",
                                     help="Ingrese la longitud en grados decimales")
        
        with col2:
            año = st.number_input("Año", min_value=2000, max_value=2100, value=año)
            meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            mes = st.selectbox("Mes", options=meses, index=meses.index(mes) if mes in meses else 0)
        
        st.subheader("Superficie")
        col1, col2 = st.columns(2)
        
        with col1:
            sup_total = st.number_input("Superficie Total (ha)", min_value=0, value=int(float(sup_total)) if sup_total != "" else 0)
        
        with col2:
            max_val = int(float(sup_total)) if sup_total and float(sup_total) > 0 else 1000000
            sup_vt = st.number_input("Superficie Vacas Totales (ha)", 
                                    min_value=0, 
                                    max_value=max_val,
                                    value=int(float(sup_vt)) if sup_vt != "" else 0)
        
        st.subheader("Producción")
        col1, col2 = st.columns(2)
        
        with col1:
            produccion_ind = st.number_input("Producción Individual (litros/vaca/día)", 
                                           min_value=0.0, value=float(produccion_ind) if produccion_ind != "" else 0.0, format="%.2f")
        
        with col2:
            vacas_ordeñe = st.number_input("Vacas en Ordeñe", min_value=0, value=int(vacas_ordeñe) if vacas_ordeñe != "" else 0)
        
        st.subheader("Destino de la Leche (%)")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            venta_industria = st.number_input("Venta a Industria (%)", min_value=0, max_value=100, value=int(venta_industria))
        
        with col2:
            uso_queseria = st.number_input("Uso en Quesería (%)", min_value=0, max_value=100, value=int(uso_queseria))
        
        with col3:
            descarte = st.number_input("Descarte (%)", min_value=0, max_value=100, value=int(descarte))
        
        # Check if percentages sum to 100
        if venta_industria + uso_queseria + descarte != 100:
            st.warning("⚠️ La suma de los porcentajes debe ser 100%")
        
        st.subheader("Calidad de la Leche")
        col1, col2 = st.columns(2)
        
        with col1:
            porcentaje_proteina = st.number_input("Porcentaje de Proteína (%)", 
                                              min_value=0.0, max_value=10.0, 
                                              value=float(porcentaje_proteina) if porcentaje_proteina != "" else 0.0, 
                                              format="%.2f")
        
        with col2:
            porcentaje_grasa = st.number_input("Porcentaje de Grasa (%)", 
                                           min_value=0.0, max_value=10.0, 
                                           value=float(porcentaje_grasa) if porcentaje_grasa != "" else 0.0, 
                                           format="%.2f")
        
        submitted = st.form_submit_button("Guardar Datos Generales")
        
        if submitted:
            # Validate input
            validation_errors = []
            
            if not validate_text(nombre_tambo):
                validation_errors.append("El nombre del tambo es obligatorio.")
            
            if not validate_text(ciudad):
                validation_errors.append("La ciudad/localidad es obligatoria.")
            
            if not validate_numeric(sup_total, min_val=0):
                validation_errors.append("La superficie total debe ser un número positivo.")
            
            if not validate_numeric(sup_vt, min_val=0):
                validation_errors.append("La superficie de vacas totales debe ser un número positivo.")
            
            if float(sup_vt) > float(sup_total):
                validation_errors.append("La superficie de vacas totales no puede ser mayor a la superficie total.")
            
            if not validate_numeric(produccion_ind, min_val=0):
                validation_errors.append("La producción individual debe ser un número positivo.")
            
            if not validate_numeric(vacas_ordeñe, min_val=0):
                validation_errors.append("El número de vacas en ordeñe debe ser un número positivo.")
            
            if venta_industria + uso_queseria + descarte != 100:
                validation_errors.append("La suma de los porcentajes de destino de la leche debe ser 100%.")
            
            # If there are validation errors, display them and stop
            if validation_errors:
                for error in validation_errors:
                    show_validation_error(error)
                return
            
            # Create data object
            data = {
                'uuid': st.session_state.datos_uuid,
                'nombre_tambo': nombre_tambo,
                'ciudad': ciudad,
                'raza': raza,
                'latitud': latitud,
                'longitud': longitud,
                'año': año,
                'mes': mes,
                'sup_total': sup_total,
                'sup_vt': sup_vt,
                'produccion_ind': produccion_ind,
                'vacas_ordeñe': vacas_ordeñe,
                'venta_industria': venta_industria,
                'uso_queseria': uso_queseria,
                'descarte': descarte,
                'porcentaje_proteina': porcentaje_proteina,
                'porcentaje_grasa': porcentaje_grasa
            }
            
            # Create dataframe
            new_df = pd.DataFrame([data])
            
            # Save dataframe
            save_dataframe(new_df, "datos_generales.csv")
            
            # Store farm name in session state for reference in other sections
            st.session_state.farm_name = nombre_tambo
            
            # Show success message
            show_success_message("Datos guardados correctamente")
    
    # Show current data if available
    if has_existing_data:
        st.subheader("Datos actuales")
        st.dataframe(datos_df.drop(columns=['uuid']) if 'uuid' in datos_df.columns else datos_df)
