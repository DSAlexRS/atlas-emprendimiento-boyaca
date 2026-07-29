from __future__ import annotations


PROFILE_ORDER = [
    "Emergentes vulnerables de baja capacidad",
    "Emergentes con mayor articulación financiera",
    "Consolidados, densos y con mayores capacidades",
    "En transición con capacidades medias y baja densidad",
    "Tradicionales maduros con rezagos de gestión",
]

PROFILE_SHORT = {
    PROFILE_ORDER[0]: "Emergentes vulnerables",
    PROFILE_ORDER[1]: "Emergentes articulados",
    PROFILE_ORDER[2]: "Consolidados",
    PROFILE_ORDER[3]: "En transición",
    PROFILE_ORDER[4]: "Tradicionales maduros",
}

PROFILE_COLORS = {
    PROFILE_ORDER[0]: "#c55a5a",
    PROFILE_ORDER[1]: "#d28a3d",
    PROFILE_ORDER[2]: "#2d8b74",
    PROFILE_ORDER[3]: "#4778a8",
    PROFILE_ORDER[4]: "#7b668f",
}

PROFILE_SUMMARIES = {
    PROFILE_ORDER[0]: (
        "Tejido con restricciones simultáneas de escala, gestión y densidad. "
        "Predominan las unidades unipersonales y de ingresos bajos. La etiqueta "
        "describe vulnerabilidad productiva; no equivale a informalidad ni a "
        "emprendimiento por necesidad."
    ),
    PROFILE_ORDER[1]: (
        "Combina alta renovación con la mayor articulación financiera y "
        "asociativa relativa. El acceso o búsqueda de crédito ofrece una base "
        "para consolidarse, aunque persisten restricciones formales y de escala."
    ),
    PROFILE_ORDER[2]: (
        "Reúne mayor formalización, capacidades, adopción digital y densidad. "
        "Es una posición comparativamente favorable dentro de Boyacá, no una "
        "certificación de productividad o escalabilidad de todas sus unidades."
    ),
    PROFILE_ORDER[3]: (
        "Presenta capacidades internas cercanas o ligeramente superiores al "
        "promedio, pero menor masa empresarial y articulación financiera. El "
        "reto central es transformar capacidades dispersas en conexiones y mercado."
    ),
    PROFILE_ORDER[4]: (
        "Concentra mayor permanencia observada y menor renovación, junto con "
        "rezagos de gestión, escala y finanzas. Muestra que longevidad y "
        "modernización no son procesos equivalentes."
    ),
}

PROFILE_POLICY = {
    PROFILE_ORDER[0]: (
        "Gestión básica, registro, alfabetización financiera y adopción digital, "
        "con mecanismos móviles o supramunicipales donde la accesibilidad sea baja."
    ),
    PROFILE_ORDER[1]: (
        "Calidad del financiamiento, conexión comercial y fortalecimiento de redes "
        "para traducir renovación y articulación en consolidación."
    ),
    PROFILE_ORDER[2]: (
        "Innovación, sofisticación de servicios, encadenamientos, mercados "
        "extralocales y difusión de capacidades hacia el entorno."
    ),
    PROFILE_ORDER[3]: (
        "Construcción de masa crítica, redes empresariales y canales de mercado "
        "que aprovechen las capacidades ya presentes."
    ),
    PROFILE_ORDER[4]: (
        "Modernización contable y digital, sucesión, renovación comercial y "
        "valorización del conocimiento acumulado."
    ),
}

DOMAIN_COLUMNS = {
    "Madurez y permanencia": "madurez_permanencia_observada",
    "Formalización y gestión": "formalizacion_gestion",
    "Escala y capacidades": "escala_capacidades",
    "Finanzas y redes": "finanzas_redes",
    "Densidad emprendedora": "densidad_emprendedora",
}

INDICATOR_COLUMNS = {
    "Unidades con menos de 3 años (%)": "pct_operacion_menos_3_anios",
    "Unidades con más de 10 años (%)": "pct_operacion_mas_10_anios",
    "Unidades con RUT (%)": "pct_rut_si",
    "Sin registros contables (%)": "pct_no_lleva_registros_contables",
    "Unidades de una persona (%)":
        "pct_ue_un_solo_trabajador_sociodemografico",
    "Ingresos hasta $10 millones (%)": "pct_ue_ingresos_hasta_10m_2023",
    "Propietarios con educación superior (%)":
        "pct_propietarios_educacion_superior",
    "Reporte medio de pagos digitales (%)":
        "promedio_reporte_medios_digitales",
    "Solicitó crédito (%)": "pct_solicito_credito_si",
    "Pertenece a asociación (%)":
        "pct_asociacion_productores_comerciantes_si",
}

SECTOR_COLUMNS = {
    "Primario y extractivo": "pct_ciiu_primario_extractivo_sectorial_2023",
    "Manufactura": "pct_ciiu_manufactura_sectorial_2023",
    "Infraestructura y logística":
        "pct_ciiu_infraestructura_logistica_sectorial_2023",
    "Comercio": "pct_ciiu_comercio_sectorial_2023",
    "Alojamiento y comidas": "pct_ue_alojamiento_comidas_sectorial_2023",
    "Servicios empresariales y conocimiento":
        "pct_ciiu_servicios_empresariales_conocimiento_sectorial_2023",
    "Servicios sociales y personales":
        "pct_ciiu_servicios_sociales_personales_sectorial_2023",
}

DISTANCE_ORDER = [
    "Muy próximo",
    "Próximo",
    "Intermedio",
    "Lejano",
    "Muy lejano",
]

DISTANCE_COLORS = {
    "Muy próximo": "#173b57",
    "Próximo": "#356a85",
    "Intermedio": "#6d98aa",
    "Lejano": "#a6bcc3",
    "Muy lejano": "#d8e1e2",
}

DOMAIN_EXPLANATIONS = {
    "Madurez y permanencia": (
        "Contrasta renovación reciente y presencia de unidades con más de diez "
        "años. No estima supervivencia."
    ),
    "Formalización y gestión": (
        "Combina forma jurídica, RUT y registros contables como señales "
        "diferentes de organización."
    ),
    "Escala y capacidades": (
        "Integra tamaño laboral, nivel de ingresos, educación de propietarios y "
        "uso de medios digitales."
    ),
    "Finanzas y redes": (
        "Resume solicitud de crédito y pertenencia a asociaciones. No mide monto "
        "ni calidad del financiamiento."
    ),
    "Densidad emprendedora": (
        "Unidades económicas urbanas visibles por cada mil habitantes; controla "
        "parcialmente el tamaño municipal."
    ),
}

