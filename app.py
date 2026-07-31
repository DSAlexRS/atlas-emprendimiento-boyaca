from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from src.charts import (
    PLOT_CONFIG,
    accessibility_scatter,
    distance_domain_lines,
    distance_map,
    domain_comparison,
    domain_radar,
    profile_distribution,
    profile_map,
    sector_bar,
)
from src.content import (
    DISTANCE_ORDER,
    DOMAIN_COLUMNS,
    DOMAIN_EXPLANATIONS,
    INDICATOR_COLUMNS,
    MUNICIPALITY_INDICATOR_GROUPS,
    MUNICIPALITY_UNIVERSES,
    PROFILE_COLORS,
    PROFILE_ORDER,
    PROFILE_POLICY,
    PROFILE_SHORT,
    PROFILE_SUMMARIES,
)
from src.data import (
    apply_filters,
    fmt_decimal,
    fmt_integer,
    load_associations,
    load_data,
    load_geojson,
    load_moran,
    load_spatial_summary,
)

PROFILE_FILTER_LABELS = {
    profile: f"{marker} {PROFILE_SHORT[profile]}"
    for profile, marker in zip(
        PROFILE_ORDER,
        ["🔴", "🟠", "🟢", "🔵", "🟣"],
    )
}


st.set_page_config(
    page_title="Atlas del tejido emprendedor de Boyacá",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="auto",
)

st.markdown(
    """
    <style>
    :root {
        --ink: #172b38;
        --muted: #5b6d78;
        --paper: #f6f3ec;
        --card: #ffffff;
        --line: #dce3e7;
        --brand: #173b57;
        --accent: #d28a3d;
    }
    .stApp {
        background:
            radial-gradient(circle at 88% 4%, rgba(210,138,61,.12), transparent 22rem),
            linear-gradient(180deg, #f9faf8 0%, #f4f6f5 100%);
        color: var(--ink);
    }
    [data-testid="stSidebar"] {
        background: #102b3c;
        border-right: 1px solid rgba(255,255,255,.08);
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #f4f7f8;
    }
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #c8d4da;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label {
        padding: .35rem .45rem;
        border-radius: .45rem;
    }
    [data-testid="stSidebar"] button[data-variant="pills"] {
        border-color: rgba(255,255,255,.28);
        background: rgba(255,255,255,.07);
    }
    [data-testid="stSidebar"] button[data-variant="pills"] p {
        color: #eef4f6 !important;
    }
    [data-testid="stSidebar"] button[data-variant="pills"][aria-pressed="true"] {
        background: rgba(255,255,255,.08);
        border-color: rgba(255,255,255,.32);
    }
    [data-testid="stSidebar"] button[data-variant="pills"][aria-pressed="true"] p {
        color: #f4f7f8 !important;
        font-weight: 700;
    }
    [data-testid="stSidebar"] button[data-variant="pills"][aria-pressed="false"] {
        background: #f4f7f8;
        border-color: #f4f7f8;
    }
    [data-testid="stSidebar"] button[data-variant="pills"][aria-pressed="false"] p,
    [data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] p {
        color: #173b57 !important;
        font-weight: 650;
    }
    .block-container {
        max-width: 1420px;
        padding-top: 1.15rem;
        padding-bottom: 4rem;
    }
    .hero {
        padding: 1.15rem 1.4rem 1rem;
        border: 1px solid var(--line);
        border-left: 5px solid var(--accent);
        border-radius: 1rem;
        background: rgba(255,255,255,.90);
        box-shadow: 0 10px 28px rgba(23,43,56,.06);
        margin-bottom: 1.2rem;
    }
    .hero-kicker {
        margin: 0 0 .35rem;
        color: #7e5726;
        font-size: .78rem;
        font-weight: 750;
        letter-spacing: .12em;
        text-transform: uppercase;
    }
    .hero h1 {
        margin: 0;
        color: var(--ink);
        font-size: clamp(1.85rem, 3.4vw, 2.75rem);
        line-height: 1.03;
        letter-spacing: -.035em;
    }
    .hero p {
        margin: .7rem 0 0;
        max-width: 920px;
        color: var(--muted);
        font-size: .98rem;
        line-height: 1.55;
    }
    .section-kicker {
        color: #7e5726;
        font-size: .76rem;
        font-weight: 760;
        letter-spacing: .11em;
        text-transform: uppercase;
        margin: .3rem 0 .2rem;
    }
    .insight {
        background: #edf3f4;
        border: 1px solid #d2dee2;
        border-radius: .8rem;
        padding: 1rem 1.1rem;
        color: #274553;
        line-height: 1.5;
        margin: .6rem 0 1rem;
    }
    .filter-summary {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        margin: .15rem 0 1rem;
        padding: .72rem .9rem;
        background: rgba(255,255,255,.76);
        border: 1px solid var(--line);
        border-radius: .72rem;
        color: var(--muted);
        font-size: .88rem;
    }
    .filter-summary strong { color: var(--brand); }
    .profile-card {
        background: white;
        border: 1px solid var(--line);
        border-radius: .9rem;
        padding: 1.05rem 1.15rem;
        min-height: 168px;
        box-shadow: 0 7px 18px rgba(23,43,56,.045);
    }
    .profile-card h3 {
        margin: .15rem 0 .45rem;
        font-size: 1.06rem;
        color: var(--ink);
    }
    .profile-card p {
        color: var(--muted);
        font-size: .91rem;
        line-height: 1.45;
    }
    [data-testid="stMetric"] {
        background: rgba(255,255,255,.92);
        border: 1px solid var(--line);
        padding: .85rem 1rem;
        border-radius: .8rem;
        box-shadow: 0 5px 16px rgba(23,43,56,.04);
    }
    [data-testid="stMetricLabel"] { color: var(--muted); }
    [data-testid="stMetricValue"] { color: var(--ink); }
    div[data-testid="stDataFrame"] {
        border: 1px solid var(--line);
        border-radius: .65rem;
        overflow: hidden;
    }
    .method-box {
        border-top: 3px solid var(--brand);
        background: white;
        padding: 1rem 1.1rem;
        border-radius: .65rem;
        box-shadow: 0 6px 18px rgba(23,43,56,.04);
        min-height: 150px;
        margin-bottom: .85rem;
    }
    .method-box strong { color: var(--brand); }
    .small-note {
        color: var(--muted);
        font-size: .84rem;
        line-height: 1.45;
    }
    .footer {
        margin-top: 2.8rem;
        border-top: 1px solid var(--line);
        padding-top: 1rem;
        color: var(--muted);
        font-size: .82rem;
    }
    h2, h3 { color: var(--ink); letter-spacing: -.015em; }
    @media (max-width: 760px) {
        .block-container {
            padding: .7rem .8rem 3rem;
        }
        .hero {
            padding: .95rem 1rem .9rem;
            margin-bottom: .85rem;
        }
        .hero h1 {
            font-size: clamp(1.55rem, 8vw, 2.05rem);
            line-height: 1.08;
        }
        .hero p {
            font-size: .91rem;
        }
        .filter-summary {
            display: block;
            padding: .7rem .8rem;
        }
        .filter-summary span {
            display: block;
        }
        .filter-summary span + span {
            margin-top: .35rem;
        }
        .method-box,
        .profile-card {
            min-height: auto;
        }
        [data-testid="stMetric"] {
            padding: .72rem .82rem;
        }
        [data-testid="stSidebar"] {
            width: min(86vw, 330px);
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def profile_means(data: pd.DataFrame) -> pd.DataFrame:
    municipal_indicators = [
        column
        for group in MUNICIPALITY_INDICATOR_GROUPS.values()
        for column in group.values()
    ]
    numeric = list(
        dict.fromkeys(
            list(DOMAIN_COLUMNS.values())
            + list(INDICATOR_COLUMNS.values())
            + municipal_indicators
        )
    )
    return (
        data.assign(perfil_texto=data["perfil"].astype(str))
        .groupby("perfil_texto", observed=True)[numeric]
        .mean()
        .reindex(PROFILE_ORDER)
    )


def page_header(kicker: str, title: str, text: str) -> None:
    st.markdown(
        f"""
        <section class="hero">
            <p class="hero-kicker">{kicker}</p>
            <h1>{title}</h1>
            <p>{text}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def reset_sidebar_filters() -> None:
    st.session_state["profile_filter"] = PROFILE_ORDER
    st.session_state["distance_filter"] = DISTANCE_ORDER


def reset_map_view(state_key: str) -> None:
    st.session_state[state_key] = st.session_state.get(state_key, 0) + 1


def render_overview(
    data: pd.DataFrame,
    filtered: pd.DataFrame,
    geojson: dict,
) -> None:
    page_header(
        "Atlas municipal · referencia económica 2023",
        "El tejido emprendedor de Boyacá no sigue una sola trayectoria",
        "Explore cómo se combinan madurez, formalización, capacidades, redes y "
        "densidad en 123 municipios. Los perfiles son configuraciones comparativas "
        "del tejido urbano visible, no un ranking de emprendimiento.",
    )

    is_complete = len(filtered) == len(data)
    filter_label = (
        "Vista departamental completa"
        if is_complete
        else "Vista filtrada"
    )
    st.markdown(
        f"""
        <div class="filter-summary">
            <span><strong>{filter_label}</strong> · {len(filtered)} de
            {len(data)} municipios</span>
            <span>Los municipios excluidos permanecen en gris para conservar
            el contexto territorial.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Municipios visibles", fmt_integer(len(filtered)))
    c2.metric(
        "Unidades económicas",
        fmt_integer(filtered["n_unidades_economicas_urbanas"].sum()),
    )
    c3.metric(
        "Densidad mediana",
        f"{fmt_decimal(filtered['ue_urbanas_visibles_por_1000_hab_total_2023'].median())} / mil",
    )
    c4.metric("Perfiles presentes", fmt_integer(filtered["perfil"].nunique()))

    map_title, map_action = st.columns([4.2, 1])
    with map_title:
        st.markdown("### Geografía de los perfiles")
    with map_action:
        st.button(
            "↺ Vista completa",
            key="reset_profile_map",
            on_click=reset_map_view,
            args=("profile_map_revision",),
            width="stretch",
            help="Recupera la silueta completa de Boyacá después de acercar o mover el mapa.",
        )
    if filtered.empty:
        st.warning("Los filtros actuales no dejan municipios para visualizar.")
        return
    st.plotly_chart(
        profile_map(filtered, geojson, data),
        width="stretch",
        config=PLOT_CONFIG,
        key=f"profile_map_{st.session_state.get('profile_map_revision', 0)}",
    )
    st.caption(
        "Al acercar, el mapa muestra solo el área contenida en el lienzo: no se "
        "pierden municipios. Arrastre para recorrerlo, use pantalla completa para "
        "más espacio o pulse «Vista completa» para recuperar todo Boyacá."
    )
    with st.expander(
        f"Ver los {len(filtered)} municipios de la selección",
        expanded=False,
    ):
        visible_table = filtered[
            [
                "municipio",
                "perfil",
                "tramo_distancia",
                "n_unidades_economicas_urbanas",
                "ue_urbanas_visibles_por_1000_hab_total_2023",
            ]
        ].copy()
        visible_table.columns = [
            "Municipio",
            "Perfil",
            "Distancia relativa",
            "Unidades visibles",
            "Unidades por 1.000 hab.",
        ]
        visible_table["Municipio"] = visible_table["Municipio"].str.title()
        visible_table["Perfil"] = visible_table["Perfil"].astype(str).map(
            PROFILE_SHORT
        )
        st.dataframe(
            visible_table.sort_values(["Perfil", "Municipio"]).style.format(
                {
                    "Unidades visibles": "{:,.0f}",
                    "Unidades por 1.000 hab.": "{:.1f}",
                }
            ),
            hide_index=True,
            width="stretch",
            height=330,
        )

    left, right = st.columns([1.03, 1], gap="large")
    with left:
        st.markdown("### Distribución municipal")
        st.plotly_chart(
            profile_distribution(filtered),
            width="stretch",
            config=PLOT_CONFIG,
        )
    with right:
        st.markdown("### La lectura central")
        st.markdown(
            """
            <div class="insight">
            La renovación puede coexistir con vulnerabilidad o con articulación
            financiera; la permanencia puede sostenerse sin igual acumulación de
            gestión; y la densidad no depende de manera monotónica de la cercanía a
            las grandes ciudades. El valor analítico está en la combinación.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            "El volumen total de unidades está fuertemente condicionado por la "
            "población. Por eso la tipología utiliza porcentajes, intensidades y "
            "cinco dimensiones estandarizadas."
        )

    st.markdown("### Cinco configuraciones, cinco necesidades distintas")
    columns = st.columns(5)
    counts = filtered["perfil"].astype(str).value_counts()
    for column, profile in zip(columns, PROFILE_ORDER):
        with column:
            st.markdown(
                f"""
                <div class="profile-card"
                     style="border-top: 4px solid {PROFILE_COLORS[profile]};">
                    <h3>{PROFILE_SHORT[profile]}</h3>
                    <p><strong>{int(counts.get(profile, 0))} municipios visibles</strong></p>
                    <p>{PROFILE_SUMMARIES[profile]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_profiles(data: pd.DataFrame) -> None:
    page_header(
        "Tipología municipal",
        "¿Qué distingue a cada perfil?",
        "Seleccione una configuración para leer su centroide, sus indicadores "
        "observables, los municipios que la integran y la orientación de política "
        "que sugiere. Las etiquetas resumen promedios y admiten casos fronterizos.",
    )
    selected = st.selectbox(
        "Perfil para explorar",
        PROFILE_ORDER,
        format_func=lambda value: PROFILE_SHORT[value],
    )
    subset = data[data["perfil"].astype(str).eq(selected)].copy()
    means = profile_means(data)
    selected_means = means.loc[selected].copy()
    selected_means["perfil"] = selected

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Municipios", len(subset))
    k2.metric(
        "Unidades visibles",
        fmt_integer(subset["n_unidades_economicas_urbanas"].sum()),
    )
    k3.metric(
        "Densidad media",
        fmt_decimal(
            subset["ue_urbanas_visibles_por_1000_hab_total_2023"].mean()
        ),
    )
    k4.metric(
        "Distancia mediana",
        f"{fmt_decimal(subset['distancia_lineal_nucleo_urbano_top5_km'].median())} km",
    )

    st.markdown(
        f"""
        <div class="insight"><strong>{PROFILE_SHORT[selected]}.</strong>
        {PROFILE_SUMMARIES[selected]}</div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.08, 1], gap="large")
    with left:
        st.markdown("#### Posición relativa en las cinco dimensiones")
        st.plotly_chart(
            domain_radar(selected_means),
            width="stretch",
            config=PLOT_CONFIG,
        )
        st.caption(
            "Cero representa el promedio departamental. Los valores positivos "
            "indican una posición relativa mayor en la dimensión."
        )
    with right:
        st.markdown("#### Indicadores observables del perfil")
        indicator_table = pd.DataFrame(
            {
                "Indicador": list(INDICATOR_COLUMNS),
                "Perfil": [
                    selected_means[column]
                    for column in INDICATOR_COLUMNS.values()
                ],
                "Boyacá": [
                    data[column].mean() for column in INDICATOR_COLUMNS.values()
                ],
            }
        )
        st.dataframe(
            indicator_table,
            hide_index=True,
            width="stretch",
            height=420,
            column_config={
                "Indicador": st.column_config.TextColumn(
                    "Indicador",
                    width="medium",
                ),
                "Perfil": st.column_config.NumberColumn(
                    "Perfil (%)",
                    width="small",
                    format="%.1f",
                ),
                "Boyacá": st.column_config.NumberColumn(
                    "Boyacá (%)",
                    width="small",
                    format="%.1f",
                ),
            },
        )

    st.markdown("#### Municipios pertenecientes al perfil")
    municipality_table = subset[
        [
            "municipio",
            "tipo_asignacion",
            "silueta_individual",
            "distancia_centroide",
            "tramo_distancia",
            "nodo_mas_cercano",
        ]
    ].copy()
    municipality_table.columns = [
        "Municipio",
        "Tipo de asignación",
        "Silueta",
        "Distancia al centroide",
        "Tramo de distancia",
        "Nodo aproximado",
    ]
    municipality_table["Municipio"] = municipality_table["Municipio"].str.title()
    municipality_table = municipality_table.sort_values(
        ["Tipo de asignación", "Distancia al centroide", "Municipio"]
    )
    st.dataframe(
        municipality_table.style.format(
            {"Silueta": "{:.3f}", "Distancia al centroide": "{:.3f}"}
        ),
        hide_index=True,
        width="stretch",
        height=380,
    )
    st.markdown(
        f"**Orientación de política:** {PROFILE_POLICY[selected]}"
    )


def render_accessibility(
    data: pd.DataFrame,
    filtered: pd.DataFrame,
    geojson: dict,
) -> None:
    page_header(
        "Accesibilidad y organización espacial",
        "La distancia condiciona capacidades, pero no vacía la economía local",
        "La cercanía a los principales nodos se relaciona con formalización, "
        "educación y finanzas. La densidad empresarial, en cambio, puede mantenerse "
        "en municipios alejados y revelar posibles centralidades secundarias.",
    )
    associations = load_associations()

    if filtered.empty:
        st.warning(
            "La combinación de filtros no contiene municipios. Ajusta los "
            "perfiles o las bandas de distancia en la barra lateral."
        )
        return

    st.markdown("### Tres preguntas para leer esta sección")
    reading_columns = st.columns(3)
    reading_cards = [
        (
            "1. ¿Qué tan lejos está?",
            "La distancia aproxima la accesibilidad al núcleo urbano grande más "
            "cercano. No representa tiempo de viaje ni calidad vial.",
        ),
        (
            "2. ¿Qué cambia con la distancia?",
            "Las correlaciones muestran si una capacidad tiende a aumentar o "
            "disminuir al alejarse. Describen asociación, no causalidad.",
        ),
        (
            "3. ¿Aparecen polos propios?",
            "Un municipio lejano y denso puede funcionar como centralidad local, "
            "pero confirmarlo requiere flujos de empleo, comercio y movilidad.",
        ),
    ]
    for column, (title, text) in zip(reading_columns, reading_cards):
        with column:
            st.markdown(
                f"""
                <div class="method-box">
                    <strong>{title}</strong>
                    <p>{text}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    map_title, map_action = st.columns([4.2, 1])
    with map_title:
        st.markdown("### Gradiente territorial")
    with map_action:
        st.button(
            "↺ Vista completa",
            key="reset_distance_map",
            on_click=reset_map_view,
            args=("distance_map_revision",),
            width="stretch",
            help="Recupera la silueta completa de Boyacá después de acercar o mover el mapa.",
        )
    st.plotly_chart(
        distance_map(filtered, geojson, data),
        width="stretch",
        config=PLOT_CONFIG,
        key=f"distance_map_{st.session_state.get('distance_map_revision', 0)}",
    )
    st.caption(
        "La distancia es geodésica al más cercano de los cinco núcleos con mayor "
        "población de cabecera. Es una aproximación y no equivale a tiempo de viaje."
    )

    available_metrics = {
        "Finanzas y redes": "finanzas_redes",
        "Formalización y gestión": "formalizacion_gestion",
        "Madurez y permanencia": "madurez_permanencia_observada",
        "Escala y capacidades": "escala_capacidades",
        "Densidad emprendedora": "densidad_emprendedora",
        "Unidades con RUT (%)": "pct_rut_si",
        "Propietarios con educación superior (%)":
            "pct_propietarios_educacion_superior",
        "Valor agregado por habitante":
            "va_2023_por_habitante_millones_cop",
    }
    selected_label = st.selectbox(
        "Indicador para contrastar con la distancia",
        list(available_metrics),
    )
    selected_column = available_metrics[selected_label]

    chart_col, note_col = st.columns([1.6, 0.8], gap="large")
    with chart_col:
        st.plotly_chart(
            accessibility_scatter(filtered, selected_column, selected_label),
            width="stretch",
            config=PLOT_CONFIG,
        )
    with note_col:
        match = associations[
            associations["variable"].eq(selected_column)
        ]
        if not match.empty:
            row = match.iloc[0]
            rho = float(row["rho_spearman"])
            direction = (
                "tiende a disminuir con la distancia"
                if rho < -0.10
                else "tiende a aumentar con la distancia"
                if rho > 0.10
                else "no muestra un gradiente claro"
            )
            st.metric(
                "Relación con la distancia (ρ)",
                fmt_decimal(rho, 3),
                help=(
                    "ρ de Spearman varía entre -1 y 1. El signo indica la dirección "
                    "y el valor absoluto, la intensidad de la asociación monotónica."
                ),
            )
            st.markdown(
                f"**Lectura:** relación {row['magnitud'].lower()}; el indicador "
                f"{direction}."
            )
            with st.expander("Ver detalle estadístico"):
                p_value = (
                    "< 0,001"
                    if row["p_ajustado_bonferroni"] < 0.001
                    else fmt_decimal(row["p_ajustado_bonferroni"], 3)
                )
                st.markdown(
                    f"**ρ de Spearman:** {fmt_decimal(rho, 3)}  \n"
                    f"**p ajustado por comparaciones múltiples:** {p_value}"
                )
                st.caption(
                    "El ajuste reduce el riesgo de declarar asociaciones por azar "
                    "cuando se examinan varios indicadores."
                )
        else:
            st.info(
                "Este indicador se muestra para exploración; no forma parte de "
                "la tabla confirmatoria de asociaciones."
            )
        st.markdown(
            '<p class="small-note">Una correlación no estima un impacto causal. '
            "Población, infraestructura, historia productiva y composición "
            "sectorial pueden intervenir simultáneamente.</p>",
            unsafe_allow_html=True,
        )

    st.markdown("### Cómo cambian conjuntamente las dimensiones")
    st.plotly_chart(
        distance_domain_lines(data),
        width="stretch",
        config=PLOT_CONFIG,
    )

    st.markdown("### Candidatos exploratorios a centralidades secundarias")
    poles = (
        data[data["candidato_polo_secundario"]]
        .sort_values(
            "ue_urbanas_visibles_por_1000_hab_total_2023",
            ascending=False,
        )
        .copy()
    )
    poles_table = poles[
        [
            "municipio",
            "perfil",
            "nodo_mas_cercano",
            "distancia_lineal_nucleo_urbano_top5_km",
            "ue_urbanas_visibles_por_1000_hab_total_2023",
            "formalizacion_gestion",
            "finanzas_redes",
        ]
    ]
    poles_table.columns = [
        "Municipio",
        "Perfil",
        "Nodo aproximado",
        "Distancia (km)",
        "Unidades por 1.000 hab.",
        "Formalización",
        "Finanzas y redes",
    ]
    poles_table["Municipio"] = poles_table["Municipio"].str.title()
    st.dataframe(
        poles_table.style.format(
            {
                "Distancia (km)": "{:.1f}",
                "Unidades por 1.000 hab.": "{:.1f}",
                "Formalización": "{:.2f}",
                "Finanzas y redes": "{:.2f}",
            }
        ),
        hide_index=True,
        width="stretch",
    )
    st.caption(
        "La selección identifica municipios muy alejados con alta densidad. "
        "Confirmar una centralidad exige flujos de empleo, comercio, servicios y movilidad."
    )

    st.markdown("### ¿Los municipios parecidos tienden a estar cerca?")
    moran = load_moran()
    spatial = load_spatial_summary().set_index("indicador")["valor"]
    c1, c2, c3 = st.columns(3)
    c1.metric(
        "Mayor concentración espacial",
        fmt_decimal(moran["I_Moran"].max(), 3),
        "Formalización y gestión",
        help=(
            "Corresponde al mayor I de Moran entre las dimensiones. Valores "
            "positivos indican que municipios con resultados parecidos tienden a "
            "ubicarse cerca."
        ),
    )
    c2.metric(
        "Fronteras del mismo perfil",
        "36,2%",
        "20,7% esperado",
    )
    c3.metric(
        "Coincidencia con regiones continuas",
        fmt_decimal(spatial["ARI global"], 3),
        "ARI bajo",
        help=(
            "Compara los perfiles empresariales con una regionalización que obliga "
            "a unir municipios vecinos. Un valor bajo indica que responden a "
            "preguntas territoriales distintas."
        ),
    )
    st.markdown(
        """
        <div class="insight">
        La geografía importa, pero no produce cinco regiones empresariales
        naturales. Los municipios del mismo perfil son vecinos con mayor frecuencia
        que bajo azar; aun así, cada perfil reaparece en varias partes del
        departamento y pierde homogeneidad cuando se exige continuidad.
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("Cómo se obtienen estos tres resultados"):
        st.markdown(
            """
            - **Concentración espacial (I de Moran):** pregunta si municipios con
              valores similares en una dimensión tienden a localizarse cerca.
            - **Fronteras del mismo perfil:** compara cuántos pares de municipios
              vecinos comparten perfil frente a lo esperado por azar.
            - **Coincidencia con regiones continuas (ARI):** contrasta la tipología
              empresarial con otra clasificación que obliga a formar bloques
              geográficos conectados.

            Ninguna de estas medidas prueba que la proximidad produzca el perfil.
            """
        )


def render_municipality(data: pd.DataFrame) -> None:
    page_header(
        "Ficha municipal",
        "Un municipio, leído dentro de su contexto",
        "Compare el municipio con el promedio de su perfil y explore su estructura "
        "productiva. La ficha evita convertir una etiqueta agregada en una "
        "descripción rígida.",
    )
    display_names = {
        row.municipio.title(): row.municipio
        for row in data[["municipio"]].itertuples(index=False)
    }
    selected_display = st.selectbox(
        "Municipio",
        sorted(display_names),
        index=sorted(display_names).index("Tunja")
        if "Tunja" in display_names
        else 0,
    )
    selected = display_names[selected_display]
    row = data[data["municipio"].eq(selected)].iloc[0]
    profile = str(row["perfil"])
    means = profile_means(data).loc[profile]

    st.markdown(
        f"""
        <div class="insight"><strong>{selected_display}</strong> pertenece al perfil
        <strong>{PROFILE_SHORT[profile]}</strong>. {PROFILE_SUMMARIES[profile]}</div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    c1.metric(
        "Unidades visibles",
        fmt_integer(row["n_unidades_economicas_urbanas"]),
    )
    c2.metric(
        "Población 2023",
        fmt_integer(row["poblacion_total_2023"]),
        help=(
            "Se usa 2023 para mantener el mismo año de referencia económica del "
            "subconjunto CENU y del valor agregado empleado en las comparaciones."
        ),
    )
    c3.metric(
        "Unidades por 1.000 hab.",
        fmt_decimal(row["ue_urbanas_visibles_por_1000_hab_total_2023"]),
    )
    c4, c5 = st.columns(2)
    c4.metric(
        "Distancia al nodo",
        f"{fmt_decimal(row['distancia_lineal_nucleo_urbano_top5_km'])} km",
    )
    c5.metric(
        "VA 2023 por habitante",
        f"${fmt_decimal(row['va_2023_por_habitante_millones_cop'], 2)} M",
        help=(
            "Valor agregado municipal 2023 dividido por la población proyectada "
            "de 2023. Es contexto externo y no determina el perfil."
        ),
    )
    st.caption(
        "La ficha alinea población y valor agregado con 2023, año de referencia "
        "económica de las variables CENU utilizadas. La recolección ocurrió entre "
        "2024 y comienzos de 2025."
    )

    left, right = st.columns([1.05, 1], gap="large")
    with left:
        st.markdown("#### Municipio frente al promedio de su perfil")
        st.plotly_chart(
            domain_comparison(row, means),
            width="stretch",
            config=PLOT_CONFIG,
        )
    with right:
        st.markdown("#### Estructura productiva urbana visible")
        st.plotly_chart(
            sector_bar(row),
            width="stretch",
            config=PLOT_CONFIG,
        )

    st.markdown("#### Radiografía ampliada del tejido empresarial")
    st.caption(
        "Explore cada bloque por separado. Las variables adicionales enriquecen "
        "la lectura municipal, pero no determinan el perfil asignado."
    )
    department_means = data.select_dtypes(include="number").mean()
    tabs = st.tabs(list(MUNICIPALITY_INDICATOR_GROUPS))
    for tab, (group_name, indicators_group) in zip(
        tabs, MUNICIPALITY_INDICATOR_GROUPS.items()
    ):
        with tab:
            rows = []
            for label, column in indicators_group.items():
                value = float(row[column])
                profile_reference = float(means[column])
                department_reference = float(department_means[column])
                rows.append(
                    {
                        "Indicador": label,
                        "Municipio": value,
                        "Perfil": profile_reference,
                        "Boyacá": department_reference,
                        "Brecha Boyacá": value - department_reference,
                    }
                )
            indicators = pd.DataFrame(rows)
            st.dataframe(
                indicators.style.format(
                    {
                        "Municipio": "{:.1f}",
                        "Perfil": "{:.1f}",
                        "Boyacá": "{:.1f}",
                        "Brecha Boyacá": "{:+.1f}",
                    }
                ),
                hide_index=True,
                width="stretch",
            )

    universe_rows = [
        {
            "Universo temático": label,
            "Unidades observadas": int(round(row[column])),
        }
        for label, column in MUNICIPALITY_UNIVERSES.items()
    ]
    universe_table = pd.DataFrame(universe_rows)
    small_universes = universe_table[
        universe_table["Unidades observadas"] < 30
    ]
    if not small_universes.empty:
        st.warning(
            f"{len(small_universes)} bloque(s) de esta ficha tienen menos de "
            "30 observaciones. Interprete sus porcentajes con especial cautela."
        )
        with st.expander("Ver alertas de cobertura"):
            st.dataframe(
                small_universes,
                hide_index=True,
                width="stretch",
            )
    else:
        st.caption(
            "Sin alertas por universos pequeños: todos los bloques temáticos de "
            "esta ficha reúnen al menos 30 observaciones."
        )
    with st.expander("Nota sobre los denominadores"):
        st.markdown(
            "Los universos cambian entre módulos del CENU; por eso porcentajes de "
            "filas distintas no siempre comparten el mismo denominador. IVA y "
            "renta excluyen la categoría «sin información»."
        )

    assignment_text = {
        "representativa": "cercana al centroide de su perfil",
        "intermedia": "con pertenencia intermedia",
        "fronteriza": "fronteriza respecto a otros perfiles",
    }.get(str(row["tipo_asignacion"]), "con asignación descriptiva")
    st.markdown(
        f"""
        <div class="small-note">
        La asignación de {selected_display} es <strong>{assignment_text}</strong>.
        Su silueta individual es {row['silueta_individual']:.3f} y su margen frente
        al segundo centroide es {row['margen_pertenencia']:.3f}. Estos valores
        expresan nitidez estadística, no desempeño administrativo.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_methodology(data: pd.DataFrame) -> None:
    page_header(
        "Método y alcance",
        "Qué puede —y qué no puede— decir este atlas",
        "El tablero traduce los notebooks y el artículo a una exploración pública. "
        "Todas las cifras son municipales, descriptivas y reproducibles.",
    )

    st.markdown("### Cinco dimensiones con igual peso")
    domain_items = list(DOMAIN_EXPLANATIONS.items())
    for row_items, columns in [
        (domain_items[:3], st.columns(3)),
        (domain_items[3:], st.columns(2)),
    ]:
        for column, (domain, explanation) in zip(columns, row_items):
            with column:
                st.markdown(
                    f"""
                    <div class="method-box">
                        <strong>{domain}</strong>
                        <p>{explanation}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("### Ruta analítica")
    st.markdown(
        """
        1. Se reconstruyeron porcentajes municipales con el universo temático
           correspondiente.
        2. Doce indicadores se estandarizaron, orientaron y resumieron en cinco
           dimensiones equilibradas.
        3. K-means produjo cinco perfiles interpretables; Ward y mezclas gaussianas
           sirvieron como contraste.
        4. Las doce variables directas, la estabilidad y los universos pequeños
           evaluaron sensibilidad.
        5. Gestión contable, activos, remuneración, IVA y renta se probaron en
           una auditoría adicional; enriquecen la ficha, pero no reemplazan la
           tipología porque sus mejoras estadísticas fueron parciales.
        6. Población, valor agregado, actividad CIIU y distancia se analizaron
           después, sin formar los perfiles.
        7. Moran, acuerdo vecinal y regionalización contigua examinaron la
           organización espacial.
        """
    )

    left, right = st.columns(2, gap="large")
    with left:
        st.markdown("### Límites de interpretación")
        st.markdown(
            """
            - La unidad de análisis es el municipio, no cada empresario.
            - El CENU representa unidades urbanas visibles dentro de su cobertura.
            - Persona natural, bajos ingresos o una sola persona no conforman una
              tasa oficial de informalidad.
            - Más de diez años de operación no es una tasa de supervivencia.
            - Pagos digitales no constituyen una medición de innovación.
            - Las asociaciones espaciales no identifican efectos causales.
            """
        )
    with right:
        st.markdown("### Referencia temporal")
        st.markdown(
            """
            - **CENU:** recolección entre 2024 y comienzos de 2025; las variables
              económicas territoriales utilizadas tienen referencia 2023.
            - **Población:** proyección municipal 2023 para construir tasas
              contemporáneas a esa referencia.
            - **Valor agregado:** 2023 para la comparación principal. La serie
              oficial ya ofrece 2024 provisional, que se reserva como contexto
              posterior y no reemplaza silenciosamente la referencia del estudio.
            - **Geometría:** Marco Geoestadístico Nacional 2024.
            """
        )
        st.info(
            "El valor agregado municipal no es la suma directa de las unidades "
            "censadas y se mantiene fuera del clustering."
        )

    st.markdown("### Glosario para interpretar el tablero")
    glossary = pd.DataFrame(
        [
            (
                "Perfil municipal",
                "Grupo de municipios estadísticamente parecidos; no es un ranking.",
            ),
            (
                "Puntaje estandarizado",
                "Posición respecto al promedio de Boyacá; cero es el promedio.",
            ),
            (
                "ρ de Spearman",
                "Dirección e intensidad de una relación monotónica con la distancia.",
            ),
            (
                "I de Moran",
                "Grado en que valores municipales parecidos se agrupan espacialmente.",
            ),
            (
                "ARI",
                "Coincidencia entre dos clasificaciones, descontando el acuerdo por azar.",
            ),
            (
                "Centralidad secundaria",
                "Candidato lejano con densidad alta; requiere validación con flujos reales.",
            ),
        ],
        columns=["Concepto", "Lectura sencilla"],
    )
    st.dataframe(
        glossary,
        hide_index=True,
        width="stretch",
        column_config={
            "Concepto": st.column_config.TextColumn(width="small"),
            "Lectura sencilla": st.column_config.TextColumn(width="large"),
        },
    )

    st.markdown("### Descargar la base pública del tablero")
    export = data.copy()
    export["perfil"] = export["perfil"].astype(str)
    export["tramo_distancia"] = export["tramo_distancia"].astype(str)
    st.download_button(
        "Descargar CSV municipal",
        data=export.to_csv(index=False).encode("utf-8-sig"),
        file_name="atlas_emprendimiento_boyaca_municipios.csv",
        mime="text/csv",
        width="content",
    )
    st.caption(
        "La base contiene únicamente información municipal agregada y no incluye "
        "datos personales."
    )


data = load_data()
geojson = load_geojson()
selected_profiles = st.session_state.get("profile_filter", PROFILE_ORDER)
selected_distance = st.session_state.get("distance_filter", DISTANCE_ORDER)

with st.sidebar:
    st.markdown("## ◈ Boyacá emprende")
    st.caption("Atlas del tejido emprendedor urbano visible")
    page = st.radio(
        "Explorar",
        [
            "Panorama territorial",
            "Perfiles municipales",
            "Accesibilidad territorial",
            "Ficha municipal",
            "Método y alcance",
        ],
        label_visibility="collapsed",
    )
    st.divider()
    if page in {"Panorama territorial", "Accesibilidad territorial"}:
        st.markdown("#### Filtros territoriales")
        selected_profiles = st.pills(
            "Perfiles",
            PROFILE_ORDER,
            selection_mode="multi",
            default=PROFILE_ORDER,
            format_func=lambda value: PROFILE_FILTER_LABELS[value],
            key="profile_filter",
            width="stretch",
        )
        selected_distance = st.pills(
            "Distancia relativa",
            DISTANCE_ORDER,
            selection_mode="multi",
            default=DISTANCE_ORDER,
            key="distance_filter",
            width="stretch",
        )
        st.button(
            "Restablecer filtros",
            on_click=reset_sidebar_filters,
            width="stretch",
        )
        st.caption(
            f"{len(selected_profiles)} de {len(PROFILE_ORDER)} perfiles · "
            f"{len(selected_distance)} de {len(DISTANCE_ORDER)} tramos activos."
        )
    elif page == "Perfiles municipales":
        st.markdown("#### Lectura de perfiles")
        st.caption(
            "Esta sección compara un perfil a la vez con el promedio "
            "departamental y conserva los 123 municipios."
        )
    elif page == "Ficha municipal":
        st.markdown("#### Consulta municipal")
        st.caption(
            "Seleccione un municipio en el contenido principal para compararlo "
            "con el promedio de su perfil."
        )
    else:
        st.markdown("#### Alcance")
        st.caption(
            "Esta sección documenta las decisiones, fuentes y límites "
            "interpretativos del atlas."
        )
    st.divider()
    st.caption("123 municipios · referencia económica 2023")

if not selected_profiles or not selected_distance:
    filtered = data.iloc[0:0].copy()
else:
    filtered = apply_filters(data, selected_profiles, selected_distance)

if page == "Panorama territorial":
    render_overview(data, filtered, geojson)
elif page == "Perfiles municipales":
    render_profiles(data)
elif page == "Accesibilidad territorial":
    render_accessibility(data, filtered, geojson)
elif page == "Ficha municipal":
    render_municipality(data)
else:
    render_methodology(data)

st.markdown(
    """
    <footer class="footer">
    Elaboración propia con resultados agregados del Censo Económico Nacional
    Urbano, población, valor agregado municipal y geometría DANE. Este recurso
    acompaña una investigación académica y no constituye una clasificación
    oficial de desempeño municipal.
    </footer>
    """,
    unsafe_allow_html=True,
)
