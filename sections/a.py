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


        c
                errors.append("Debe declararse al menos un destino de leche (lts/día).")