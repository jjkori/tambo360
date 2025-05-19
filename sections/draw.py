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

    recurso_forrajero = st.selectbox(
        "Tipo de recurso forrajero presente",
        opciones_recurso,
        index=opciones_recurso.index(area) if area in opciones_recurso else len(opciones_recurso) - 1
    )

    if recurso_forrajero == "Otros":
        recurso_otro = st.text_input("Especificar otro recurso forrajero", value=area)
        area = recurso_otro
    else:
        area = recurso_forrajero

    composicion = st.text_area("Mezcla de pastura o composición del pastizal (opcional)")

    hectareas = st.number_input("Hectáreas", min_value=0.0, step=0.1, value=float(hectareas))