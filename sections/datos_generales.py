import streamlit as st
from datetime import datetime
import pandas as pd
from utils import save_dataframe, load_dataframe, validate_numeric, validate_percentage, validate_text, generate_uuid, show_validation_error, show_success_message

CSV_PATH = "datos_generales.csv"

def _save_data(data):
    """Append a new row to the CSV and reset session state."""
    df = pd.DataFrame([data])
    save_dataframe(df, CSV_PATH)
    show_success_message("Datos guardados correctamente")
    # reset
    st.session_state.show_datos_summary = False
    st.session_state.datos_temp_data = {}
    st.session_state.datos_uuid = generate_uuid()
    st.rerun()

def show_datos_generales():
    """Display and handle the Datos Generales form"""
    st.title("Datos Generales del Tambo")
    datos_df = load_dataframe(CSV_PATH)
    has_existing = not datos_df.empty

    # init session state
    if "datos_uuid" not in st.session_state:
        st.session_state.datos_uuid = generate_uuid()
    if "show_datos_summary" not in st.session_state:
        st.session_state.show_datos_summary = False
    if "datos_temp_data" not in st.session_state:
        st.session_state.datos_temp_data = {}


    # 1) summary mode
    if st.session_state.show_datos_summary:
        data = st.session_state.datos_temp_data
        total_prod = data["produccion_ind"] * data["vacas_ordeñe"]

        st.markdown("### ✅ Resumen de Datos Generales")
        st.markdown(f"""
        * **Tambo**: {data['nombre_tambo']}
        * **Localidad**: {data['ciudad']}
        * **Raza**: {data['raza']}
        * **Año/Mes**: {data['año']}/{data['mes']}
        * **Superficie Total**: {data['sup_total']:.2f} ha
        * **Superficie Vacas Totales**: {data['sup_vt']:.2f} ha
        * **Producción Individual**: {data['produccion_ind']:.2f} L/vaca/día
        * **Vacas en Ordeñe**: {data['vacas_ordeñe']}
        * **Producción Total**: {total_prod:.2f} L/día
        * **Venta a Industria**: {data['venta_industria']:.2f} L/día
        * **Uso en Guachera**: {data['uso_guachera']:.2f} L/día
        * **Descarte**: {data['descarte']:.2f} L/día
        * **% Proteína**: {data['porcentaje_proteina']:.2f}%
        * **% Grasa**: {data['porcentaje_grasa']:.2f}%
        """)



###########################

    # # 1) summary mode
    # if st.session_state.show_datos_summary:
    #     data = st.session_state.datos_temp_data
    #     total_prod = data["produccion_ind"] * data["vacas_ordeñe"]

    #     st.markdown("### ✅ Resumen de Datos Generales")
    #     st.markdown(f"""
    #     * **Tambo**: {data['nombre_tambo']}
    #     * **Localidad**: {data['ciudad']}
    #     * **Raza**: {data['raza']}
    #     * **Año/Mes**: {data['año']}/{data['mes']}
    #     * **Sup. Total**: {data['sup_total']:.2f} ha
    #     * **Sup. Vacas**: {data['sup_vt']:.2f} ha
    #     * **Prod. Ind.**: {data['produccion_ind']:.2f} L/vaca/d
    #     * **Vacas Ordeñe**: {data['vacas_ordeñe']}
    #     * **Prod. Total**: {total_prod:.2f} L/d
    #     * **Venta Industria**: {data['venta_industria']}%
    #     * **Uso Quesería**: {data['uso_queseria']}%
    #     * **Descarte**: {data['descarte']}%
    #     * **Proteína**: {data['porcentaje_proteina']:.2f}%
    #     * **Grasa**: {data['porcentaje_grasa']:.2f}%
    #     """)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("📝 Confirmar y guardar", key="confirm_datos"):
                _save_data(data)
        with c2:
            if st.button("↩ Volver y editar", key="back_datos"):
                st.session_state.show_datos_summary = False
                st.rerun()

        st.divider()
        return  # skip form below

    # 2) form mode
    # prefill logic omitted for brevity; assume variables are set:
    # nombre_tambo, ciudad, raza, año, mes, sup_total, sup_vt, produccion_ind,
    # vacas_ordeñe, venta_industria, uso_queseria, descarte,
    # porcentaje_proteina, porcentaje_grasa

    with st.form("datos_generales_form"):
        st.subheader("Información General")
        col1, col2 = st.columns(2)
        with col1:
            nombre_tambo = st.text_input("Nombre del Tambo", value=st.session_state.datos_temp_data.get('nombre_tambo', ""))
            ciudad        = st.text_input("Ciudad/Localidad", value=st.session_state.datos_temp_data.get('ciudad', ""))
            raza          = st.selectbox("Raza predominante", ["Holstein","Jersey","Cruza","Otro"], 
                                         index=["Holstein","Jersey","Cruza","Otro"].index(st.session_state.datos_temp_data.get('raza',"Holstein")))
        with col2:
            año = st.number_input("Año", 2000, 2100, value=st.session_state.datos_temp_data.get('año', 2023))
            meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
            mes = st.selectbox("Mes", meses, index=meses.index(st.session_state.datos_temp_data.get('mes',"Enero")))

        st.subheader("Superficie")
        s1, s2 = st.columns(2)
        with s1:
            sup_total = st.number_input("Superficie Total (ha)", min_value=0.0, value=st.session_state.datos_temp_data.get('sup_total',0.0), format="%.2f")
        with s2:
            sup_vt = st.number_input("Sup. Vacas Totales (ha)", min_value=0.0, max_value=sup_total or 1e6,
                                     value=st.session_state.datos_temp_data.get('sup_vt',0.0), format="%.2f")

        st.subheader("Producción")
        p1, p2 = st.columns(2)
        with p1:
            produccion_ind = st.number_input("Producción Ind. (L/vaca/día)", min_value=0.0,
                                             value=st.session_state.datos_temp_data.get('produccion_ind',0.0), format="%.2f")
        with p2:
            vacas_ordeñe = st.number_input("Vacas en Ordeñe", min_value=0,
                                           value=int(st.session_state.datos_temp_data.get('vacas_ordeñe',0)))

        
       
        #### Milk Destiny
        ###### Destino de la leche y calidad

        st.subheader("Destino de la Leche (litros/día)")

        # Litros destinados por uso
        d1, d2, d3 = st.columns(3)
        with d1:
            venta_industria_lts = st.number_input("Venta a industria (lts/día)", min_value=0.0,
                                                value=float(st.session_state.datos_temp_data.get('venta_a_industria_lts', 0)))
        with d2:
            uso_guachera_lts = st.number_input("Uso en guachera (lts/día)", min_value=0.0,
                                            value=float(st.session_state.datos_temp_data.get('uso_en_guachera_lts', 0)))
        with d3:
            descarte_lts = st.number_input("Descarte (lts/día)", min_value=0.0,
                                            value=float(st.session_state.datos_temp_data.get('descarte_lts', 0)))

        # Total destino
        total_destino_lts = venta_industria_lts + uso_guachera_lts + descarte_lts
        st.markdown(f"**Total destino declarado:** {total_destino_lts:.2f} lts/día")

        # Producción esperada
        data = st.session_state.datos_temp_data
        prod_ind = data.get('produccion_ind', 0.0)
        vacas = data.get('vacas_ordeñe', 0)
        produccion_esperada = prod_ind * vacas
        st.markdown(f"**Producción estimada:** {produccion_esperada:.2f} lts/día")

        # Comparación
        diferencia = total_destino_lts - produccion_esperada
        if abs(diferencia) > 50:
            st.error(f"⚠️ Diferencia significativa: {diferencia:+.2f} lts/día")
        else:
            st.success(f"Diferencia: {diferencia:+.2f} lts/día")

        # Producción anual
        st.subheader("Producción anual reportada")
        total_anual = st.number_input("Total leche generado (último año, litros)", min_value=0.0,
                                    value=float(data.get('total_leche_anual', 0.0)))

        # Calidad de leche
        st.subheader("Calidad de la Leche")
        q1, q2 = st.columns(2)
        with q1:
            porcentaje_proteina = st.number_input("Proteína %", 0.0, 10.0,
                                                value=float(data.get('porcentaje_proteina', 0.0)), format="%.2f")
        with q2:
            porcentaje_grasa = st.number_input("Grasa %", 0.0, 10.0,
                                            value=float(data.get('porcentaje_grasa', 0.0)), format="%.2f")

        
        
        submitted = st.form_submit_button("Revisar información antes de guardar")
        if submitted:
            errors = []
            if not validate_text(nombre_tambo):   errors.append("Nombre del tambo es obligatorio.")
            if not validate_text(ciudad):         errors.append("Ciudad/Localidad es obligatoria.")
            if not validate_numeric(sup_total):   errors.append("Superficie total debe ser ≥ 0.")
            if not validate_numeric(sup_vt):      errors.append("Sup. vacas totales debe ser ≥ 0.")
            if sup_vt > sup_total:                errors.append("Sup. vacas no puede exceder total.")
            if not validate_numeric(produccion_ind): errors.append("Producción individual debe ser ≥ 0.")
            if not validate_numeric(vacas_ordeñe):   errors.append("Vacas en ordeñe debe ser ≥ 0.")
            if (venta_industria_lts + uso_guachera_lts + descarte_lts) == 0:
                errors.append("La suma de destinos debe ser mayor a 0!.")
            if errors:
                for e in errors: show_validation_error(e)
                return

            # stash and go to summary
            st.session_state.datos_temp_data = {
                "uuid": st.session_state.datos_uuid,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "nombre_tambo": nombre_tambo,
                "ciudad": ciudad,
                "raza": raza,
                "año": año,
                "mes": mes,
                "sup_total": sup_total,
                "sup_vt": sup_vt,
                "produccion_ind": produccion_ind,
                "vacas_ordeñe": vacas_ordeñe,
                "venta_industria": venta_industria_lts,
                "uso_guachera": uso_guachera_lts,
                "descarte": descarte_lts,
                "porcentaje_proteina": porcentaje_proteina,
                "porcentaje_grasa": porcentaje_grasa
            }
            st.session_state.show_datos_summary = True
            st.rerun()

    # 3) show existing data table
   # if has_existing:
   #     st.subheader("Datos actuales")
   #     st.dataframe(datos_df.drop(columns=['uuid'], errors='ignore'))
