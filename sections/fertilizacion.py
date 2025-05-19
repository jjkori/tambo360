import streamlit as st
import pandas as pd
from utils import save_dataframe, load_dataframe, validate_numeric, validate_percentage, validate_text, generate_uuid, show_validation_error, show_success_message

def show_fertilizacion():
    st.title("Fertilización")

    df = load_dataframe("fertilizacion.csv")
    has_existing_data = not df.empty

    if "fertilizacion_uuid" not in st.session_state:
        st.session_state.fertilizacion_uuid = generate_uuid()

    if "show_fertilizacion_summary" not in st.session_state:
        st.session_state.show_fertilizacion_summary = False

    if "fertilizacion_temp_data" not in st.session_state:
        st.session_state.fertilizacion_temp_data = {}

    if st.session_state.show_fertilizacion_summary:
        data = st.session_state.fertilizacion_temp_data

        st.markdown("### ✅ Resumen de Fertilización")
        st.markdown(f"""
        ##### Información General
        * **Área Fertilizada**: {data['area']}
        * **Hectáreas**: {data['hectareas']} ha
        * **Tipo de Fertilizante**: {data['tipo']}
        * **Porcentaje del Área**: {data['porcentaje_area']}%

        ##### Aplicación
        * **Cantidad Aplicada por Hectárea**: {data['cantidad_aplicada_kg_ha']} kg/ha
        * **Cantidad Total Aplicada**: {data['cantidad_aplicada_total']} kg
        * **Método de Aplicación**: {data['metodo_aplicacion']}

        ##### Técnicas y Ajustes
        * **Uso de Inhibidores**: {data['uso_inhibidores']}
        * **Urea Protegida**: {data['urea_protegida']}
        * **Ajuste de N**: {data['ajuste_n']}
        """)

        if st.button("📝 Confirmar y guardar", key="confirm_fertilizacion", type="primary"):
            new_df = pd.DataFrame([data])
            save_dataframe(new_df, "fertilizacion.csv")
            st.session_state.fertilizacion_uuid = generate_uuid()
            st.session_state.show_fertilizacion_summary = False
            st.session_state.fertilizacion_temp_data = {}
            show_success_message("Datos guardados correctamente")
            st.rerun()

        if st.button("↩ Volver y editar", key="back_fertilizacion"):
            st.session_state.show_fertilizacion_summary = False
            st.rerun()

        st.divider()

    if not st.session_state.show_fertilizacion_summary:
        if has_existing_data and not st.session_state.fertilizacion_temp_data:
            latest_data = df.iloc[-1]
            area = latest_data.get('area', "")
            hectareas = latest_data.get('hectareas', 0.0)
            tipo = latest_data.get('tipo', "Urea")
            porcentaje_area = latest_data.get('porcentaje_area', 0)
            cantidad_aplicada_kg_ha = latest_data.get('cantidad_aplicada_kg_ha', 0.0)
            cantidad_aplicada_total = latest_data.get('cantidad_aplicada_total', 0.0)
            metodo_aplicacion = latest_data.get('metodo_aplicacion', "Voleo")
            uso_inhibidores = latest_data.get('uso_inhibidores', "No")
            urea_protegida = latest_data.get('urea_protegida', "No")
            ajuste_n = latest_data.get('ajuste_n', "No")
        elif st.session_state.fertilizacion_temp_data:
            data = st.session_state.fertilizacion_temp_data
            area = data.get('area', "")
            hectareas = data.get('hectareas', 0.0)
            tipo = data.get('tipo', "Urea")
            porcentaje_area = data.get('porcentaje_area', 0)
            cantidad_aplicada_kg_ha = data.get('cantidad_aplicada_kg_ha', 0.0)
            cantidad_aplicada_total = data.get('cantidad_aplicada_total', 0.0)
            metodo_aplicacion = data.get('metodo_aplicacion', "Voleo")
            uso_inhibidores = data.get('uso_inhibidores', "No")
            urea_protegida = data.get('urea_protegida', "No")
            ajuste_n = data.get('ajuste_n', "No")
        else:
            area = ""
            hectareas = 0.0
            tipo = "Urea"
            porcentaje_area = 0
            cantidad_aplicada_kg_ha = 0.0
            cantidad_aplicada_total = 0.0
            metodo_aplicacion = "Voleo"
            uso_inhibidores = "No"
            urea_protegida = "No"
            ajuste_n = "No"

        with st.form("fertilizacion_form"):
            st.subheader("Información General")
            col1, col2 = st.columns(2)

            with col1:
                opciones_recurso = [
                    "Pastura",
                    "Pastura Mezcla ((Pasto Ovillo, Cebadilla, Trebol)(Festuca, Achicoria, Trebol))",
                    "Pastura Alfalfa",
                    "Intersiembra",
                    "Verdeo Intersiembra",
                    "Verdeo Invierno",
                    "Verdeo Verano",
                    "Maiz para Silo/Maiz para grano",
                    "Maiz",
                    "Soja",
                    "Otros"
                ]
                recurso_forrajero = st.selectbox("Tipo de recurso forrajero presente", opciones_recurso, index=opciones_recurso.index(area) if area in opciones_recurso else len(opciones_recurso) - 1, key="recurso_forrajero")
                if recurso_forrajero == "Otros":
                    recurso_otro = st.text_input("Especificar otro recurso forrajero", value=area, key="otro_recurso")
                    area = recurso_otro
                else:
                    area = recurso_forrajero
                composicion = st.text_area("Mezcla de pastura o composición del pastizal (opcional)", key="composicion")
                hectareas = st.number_input("Hectáreas", min_value=0.0, step=1, value=float(hectareas), key="hectareas")

            with col2:
                tipo = st.selectbox("Tipo de Fertilizante", ["Urea", "Fosfato diamónico", "Nitrato de amonio", "NPK", "Orgánico", "Otro"], index=["Urea", "Fosfato diamónico", "Nitrato de amonio", "NPK", "Orgánico", "Otro"].index(tipo) if tipo in ["Urea", "Fosfato diamónico", "Nitrato de amonio", "NPK", "Orgánico", "Otro"] else 0, key="tipo_fertilizante")
                porcentaje_area = st.number_input("Porcentaje del Área (%)", min_value=0, max_value=100, value=porcentaje_area, key="porcentaje_area")

            st.subheader("Aplicación")
            col1, col2, col3 = st.columns(3)

            with col1:
                cantidad_aplicada_kg_ha = st.number_input("Cantidad Aplicada (kg/ha)", min_value=0.0, step=1, value=float(cantidad_aplicada_kg_ha), key="kg_ha")
            with col2:
                cantidad_aplicada_total = st.number_input("Cantidad Total Aplicada (kg)", min_value=0.0, step=1, value=float(cantidad_aplicada_total), key="total_kg")
            with col3:
                metodo_aplicacion = st.selectbox("Método de Aplicación", ["Voleo", "Localizado", "Fertirrigación", "Otro"], index=["Voleo", "Localizado", "Fertirrigación", "Otro"].index(metodo_aplicacion) if metodo_aplicacion in ["Voleo", "Localizado", "Fertirrigación", "Otro"] else 0, key="metodo_aplicacion")

            st.subheader("Técnicas y Ajustes")
            col1, col2, col3 = st.columns(3)

            with col1:
                uso_inhibidores = st.selectbox("¿Usa Inhibidores?", ["No", "Sí"], index=0 if uso_inhibidores == "No" else 1, key="inhibidores")
            with col2:
                urea_protegida = st.selectbox("¿Usa Urea Protegida?", ["No", "Sí"], index=0 if urea_protegida == "No" else 1, key="urea")
            with col3:
                ajuste_n = st.selectbox("¿Realiza Ajuste de N?", ["No", "Sí"], index=0 if ajuste_n == "No" else 1, key="ajuste")

            submitted = st.form_submit_button("Revisar información antes de guardar")
            if submitted:
                validation_errors = []
                if not validate_text(area, min_length=1):
                    validation_errors.append("El área fertilizada no puede estar vacía.")
                if not validate_numeric(hectareas, min_val=0):
                    validation_errors.append("Las hectáreas deben ser un número positivo.")
                if not validate_percentage(porcentaje_area):
                    validation_errors.append("El porcentaje del área debe ser un valor entre 0 y 100.")
                if not validate_numeric(cantidad_aplicada_kg_ha, min_val=0):
                    validation_errors.append("La cantidad aplicada por hectárea debe ser un número positivo.")
                if not validate_numeric(cantidad_aplicada_total, min_val=0):
                    validation_errors.append("La cantidad total aplicada debe ser un número positivo.")

                if validation_errors:
                    for error in validation_errors:
                        show_validation_error(error)
                    return

                st.session_state.fertilizacion_temp_data = {
                    'uuid': st.session_state.fertilizacion_uuid,
                    'area': area,
                    'hectareas': hectareas,
                    'tipo': tipo,
                    'porcentaje_area': porcentaje_area,
                    'cantidad_aplicada_kg_ha': cantidad_aplicada_kg_ha,
                    'cantidad_aplicada_total': cantidad_aplicada_total,
                    'metodo_aplicacion': metodo_aplicacion,
                    'uso_inhibidores': uso_inhibidores,
                    'urea_protegida': urea_protegida,
                    'ajuste_n': ajuste_n
                }

                st.session_state.show_fertilizacion_summary = True
                st.rerun()

    if has_existing_data:
        st.subheader("Datos actuales de Fertilización")
        display_df = df.drop(columns=['uuid']) if 'uuid' in df.columns else df
        st.dataframe(display_df)
        if st.button("Eliminar Última Entrada"):
            if len(df) > 0:
                df = df.iloc[:-1]
                df.to_csv("data/fertilizacion.csv", index=False)
                st.success("Última entrada eliminada. Recarga la página para ver los cambios.")
                st.rerun()
