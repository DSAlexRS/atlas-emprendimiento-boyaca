from __future__ import annotations


PROFILE_ORDER = [
    "Brechas de escala y gestión",
    "Renovación y articulación financiera",
    "Mayores capacidades y densidad",
    "Capacidades intermedias y baja densidad",
    "Permanencia con brechas de gestión",
]

PROFILE_SHORT = {profile: profile for profile in PROFILE_ORDER}

PROFILE_COLORS = {
    PROFILE_ORDER[0]: "#c55a5a",
    PROFILE_ORDER[1]: "#d28a3d",
    PROFILE_ORDER[2]: "#2d8b74",
    PROFILE_ORDER[3]: "#4778a8",
    PROFILE_ORDER[4]: "#7b668f",
}

PROFILE_SUMMARIES = {
    PROFILE_ORDER[0]: (
        "Combina restricciones relativas de escala, gestión y densidad. "
        "Predominan las unidades unipersonales y de ingresos bajos. La etiqueta "
        "describe la configuración municipal observada; no equivale a una tasa "
        "de informalidad ni a emprendimiento por necesidad."
    ),
    PROFILE_ORDER[1]: (
        "Combina mayor renovación con la mayor articulación financiera y "
        "asociativa relativa. El acceso o búsqueda de crédito ofrece una base "
        "para consolidarse, aunque persisten restricciones formales y de escala."
    ),
    PROFILE_ORDER[2]: (
        "Reúne mayores niveles relativos de formalización, capacidades, adopción digital y densidad. "
        "Es una posición comparativamente favorable dentro de Boyacá, no una "
        "certificación de productividad o escalabilidad de todas sus unidades."
    ),
    PROFILE_ORDER[3]: (
        "Presenta capacidades internas cercanas o ligeramente superiores al "
        "promedio, pero menor densidad de unidades y articulación financiera. La "
        "lectura conjunta sugiere oportunidades para fortalecer conexiones y mercado."
    ),
    PROFILE_ORDER[4]: (
        "Concentra mayor permanencia observada y menor renovación, junto con "
        "brechas relativas de gestión, escala y finanzas. Muestra que longevidad y "
        "modernización no son procesos equivalentes."
    ),
}

PROFILE_POLICY = {
    PROFILE_ORDER[0]: (
        "Fortalecimiento de gestión básica, registro, alfabetización financiera y adopción digital, "
        "con mecanismos móviles o supramunicipales donde la accesibilidad sea baja."
    ),
    PROFILE_ORDER[1]: (
        "Mejora de la calidad del financiamiento, conexión comercial y fortalecimiento de redes "
        "para traducir renovación y articulación en consolidación."
    ),
    PROFILE_ORDER[2]: (
        "Innovación, sofisticación de servicios, encadenamientos y acceso a mercados "
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
    "Densidad de unidades económicas": "densidad_emprendedora",
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

MUNICIPALITY_INDICATOR_GROUPS = {
    "Trayectoria y gestión": {
        "Unidades con menos de 3 años (%)": "pct_operacion_menos_3_anios",
        "Unidades con más de 10 años (%)": "pct_operacion_mas_10_anios",
        "Persona natural (%)": "pct_persona_natural",
        "Registro en Cámara de Comercio (%)":
            "pct_registro_camara_comercio_si",
        "RUT (%)": "pct_rut_si",
        "Gestión contable formal (%)": "pct_gestion_contable_formal",
        "Sin registros contables (%)": "pct_no_lleva_registros_contables",
    },
    "Escala y capacidades": {
        "Unidades de una persona (%)":
            "pct_ue_un_solo_trabajador_sociodemografico",
        "Ingresos hasta $10 millones (%)": "pct_ue_ingresos_hasta_10m_2023",
        "Activos fijos mayores a $50 millones (%)":
            "pct_activos_fijos_mayores_50m_2023",
        "Remuneración mayor a $10 millones (%)":
            "pct_remuneracion_mayor_10m_2023",
        "Propietarios con educación superior (%)":
            "pct_propietarios_educacion_superior",
        "Reporte medio de pagos digitales (%)":
            "promedio_reporte_medios_digitales",
    },
    "Financiación y redes": {
        "Solicitó crédito (%)": "pct_solicito_credito_si",
        "Obtuvo crédito entre solicitantes (%)":
            "pct_obtuvo_credito_entre_solicitantes",
        "Fuente formal entre fuentes reportadas (%)":
            "pct_fuente_credito_formal_entre_fuentes_reportadas",
        "Pertenece a asociación (%)":
            "pct_asociacion_productores_comerciantes_si",
        "Pertenece a cooperativa (%)": "pct_cooperativa_si",
    },
    "Inclusión, localización y tributos": {
        "Propietarias mujeres (%)": "pct_propietarias_mujeres",
        "Propietarios menores de 35 años (%)":
            "pct_propietarios_menores_35",
        "Vivienda con actividad visible (%)":
            "pct_ue_vivienda_actividad_visible",
        "Emplazamiento móvil o semifijo (%)":
            "pct_ue_emplazamiento_movil_semifijo",
        "Declaró o pagó ICA entre respuestas válidas (%)":
            "pct_ica_si_entre_respuestas_validas",
        "Declaró o pagó IVA entre respuestas válidas (%)":
            "pct_iva_si_entre_respuestas_validas",
        "Declaró o pagó renta entre respuestas válidas (%)":
            "pct_renta_si_entre_respuestas_validas",
    },
}

MUNICIPALITY_UNIVERSES = {
    "Caracterización general": "n_universo_caracterizacion",
    "Educación de propietarios": "n_universo_sociodemografico_educacion",
    "Número de trabajadores": "n_universo_sociodemografico_trabajadores",
    "Ingresos de 2023": "n_universo_sectorial_ingresos_2023",
    "Crédito": "n_universo_territorial_credito_2023",
    "Gestión contable": "n_gestion_contable",
    "Activos fijos": "n_activos_fijos",
    "Remuneración": "n_remuneracion",
    "IVA (respuestas válidas)": "n_iva_valido",
    "Renta (respuestas válidas)": "n_renta_valido",
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
    "Densidad de unidades económicas": (
        "Unidades económicas urbanas visibles por cada mil habitantes; controla "
        "parcialmente el tamaño municipal."
    ),
}
