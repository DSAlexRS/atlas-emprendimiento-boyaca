from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from .content import (
    DISTANCE_COLORS,
    DISTANCE_ORDER,
    DOMAIN_COLUMNS,
    PROFILE_COLORS,
    PROFILE_ORDER,
    PROFILE_SHORT,
    SECTOR_COLUMNS,
)


PLOT_CONFIG = {
    "displaylogo": False,
    "displayModeBar": True,
    "responsive": True,
    "scrollZoom": True,
    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
}


def context_layer(
    context_data: pd.DataFrame,
    geojson: dict,
) -> go.Choropleth:
    return go.Choropleth(
        geojson=geojson,
        locations=context_data["codigo_municipio"],
        featureidkey="properties.codigo_municipio",
        z=[0] * len(context_data),
        customdata=context_data[["municipio"]]
        .assign(municipio=context_data["municipio"].str.title())
        .to_numpy(),
        colorscale=[[0, "#e5eae8"], [1, "#e5eae8"]],
        showscale=False,
        showlegend=False,
        marker_line_color="#ffffff",
        marker_line_width=0.55,
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Fuera de la selección actual<extra></extra>"
        ),
    )


def profile_map(
    data: pd.DataFrame,
    geojson: dict,
    context_data: pd.DataFrame,
) -> go.Figure:
    plot_data = data.copy()
    plot_data["perfil_mapa"] = plot_data["perfil"].astype(str).map(PROFILE_SHORT)
    plot_data["municipio_mapa"] = plot_data["municipio"].str.title()
    plot_data["unidades_texto"] = plot_data[
        "n_unidades_economicas_urbanas"
    ].map(lambda value: f"{value:,.0f}".replace(",", "."))
    plot_data["densidad_texto"] = plot_data[
        "ue_urbanas_visibles_por_1000_hab_total_2023"
    ].map(lambda value: f"{value:.1f}".replace(".", ","))
    plot_data["distancia_texto"] = plot_data[
        "distancia_lineal_nucleo_urbano_top5_km"
    ].map(lambda value: f"{value:.1f}".replace(".", ","))
    short_colors = {
        PROFILE_SHORT[key]: value for key, value in PROFILE_COLORS.items()
    }
    colored = px.choropleth(
        plot_data,
        geojson=geojson,
        locations="codigo_municipio",
        featureidkey="properties.codigo_municipio",
        color="perfil_mapa",
        category_orders={
            "perfil_mapa": [PROFILE_SHORT[p] for p in PROFILE_ORDER]
        },
        color_discrete_map=short_colors,
        custom_data=[
            "municipio_mapa",
            "unidades_texto",
            "densidad_texto",
            "distancia_texto",
        ],
        labels={
            "n_unidades_economicas_urbanas": "Unidades visibles",
            "ue_urbanas_visibles_por_1000_hab_total_2023":
                "Unidades por 1.000 hab.",
            "distancia_lineal_nucleo_urbano_top5_km":
                "Distancia al nodo (km)",
            "perfil_mapa": "Perfil",
        },
    )
    fig = go.Figure(context_layer(context_data, geojson))
    for trace in colored.data:
        trace.update(
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Perfil: %{fullData.name}<br>"
                "Unidades visibles: %{customdata[1]}<br>"
                "Densidad: %{customdata[2]} por 1.000 hab.<br>"
                "Distancia al nodo: %{customdata[3]} km"
                "<extra></extra>"
            )
        )
        fig.add_trace(trace)
    fig.update_geos(
        fitbounds="geojson",
        visible=False,
        projection_type="mercator",
        bgcolor="rgba(0,0,0,0)",
    )
    fig.update_traces(marker_line_color="white", marker_line_width=0.55)
    fig.update_layout(
        margin=dict(l=0, r=0, t=4, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        legend_title_text="Perfil municipal",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.02,
            xanchor="left",
            x=0,
            font=dict(size=11),
        ),
        height=640,
    )
    return fig


def distance_map(
    data: pd.DataFrame,
    geojson: dict,
    context_data: pd.DataFrame,
) -> go.Figure:
    plot_data = data.copy()
    plot_data["tramo_distancia_texto"] = plot_data[
        "tramo_distancia"
    ].astype(str)
    plot_data["municipio_mapa"] = plot_data["municipio"].str.title()
    plot_data["perfil_corto"] = plot_data["perfil"].astype(str).map(PROFILE_SHORT)
    plot_data["distancia_texto"] = plot_data[
        "distancia_lineal_nucleo_urbano_top5_km"
    ].map(lambda value: f"{value:.1f}".replace(".", ","))
    colored = px.choropleth(
        plot_data,
        geojson=geojson,
        locations="codigo_municipio",
        featureidkey="properties.codigo_municipio",
        color="tramo_distancia_texto",
        category_orders={"tramo_distancia_texto": DISTANCE_ORDER},
        color_discrete_map=DISTANCE_COLORS,
        custom_data=[
            "municipio_mapa",
            "nodo_mas_cercano",
            "distancia_texto",
            "perfil_corto",
        ],
        labels={
            "tramo_distancia_texto": "Tramo",
            "nodo_mas_cercano": "Nodo aproximado",
            "distancia_lineal_nucleo_urbano_top5_km": "Distancia (km)",
            "perfil": "Perfil",
        },
    )
    fig = go.Figure(context_layer(context_data, geojson))
    for trace in colored.data:
        trace.update(
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Distancia relativa: %{fullData.name}<br>"
                "Nodo aproximado: %{customdata[1]}<br>"
                "Distancia: %{customdata[2]} km<br>"
                "Perfil: %{customdata[3]}"
                "<extra></extra>"
            )
        )
        fig.add_trace(trace)
    fig.update_geos(
        fitbounds="geojson",
        visible=False,
        projection_type="mercator",
        bgcolor="rgba(0,0,0,0)",
    )
    fig.update_traces(marker_line_color="white", marker_line_width=0.55)
    fig.update_layout(
        margin=dict(l=0, r=0, t=4, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        legend_title_text="Distancia relativa",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.02,
            xanchor="left",
            x=0,
            font=dict(size=11),
        ),
        height=640,
    )
    return fig


def profile_distribution(data: pd.DataFrame) -> go.Figure:
    counts = (
        data.assign(perfil_texto=data["perfil"].astype(str))
        .groupby("perfil_texto", observed=True)
        .size()
        .reindex(PROFILE_ORDER, fill_value=0)
        .rename("municipios")
        .reset_index()
    )
    counts["perfil_corto"] = counts["perfil_texto"].map(PROFILE_SHORT)
    fig = px.bar(
        counts,
        x="municipios",
        y="perfil_corto",
        orientation="h",
        color="perfil_texto",
        color_discrete_map=PROFILE_COLORS,
        text="municipios",
    )
    fig.update_traces(textposition="outside", hovertemplate="%{y}: %{x}<extra></extra>")
    fig.update_layout(
        showlegend=False,
        xaxis_title="Municipios",
        yaxis_title=None,
        margin=dict(l=0, r=20, t=5, b=0),
        height=330,
    )
    return fig


def domain_radar(profile_row: pd.Series) -> go.Figure:
    labels = list(DOMAIN_COLUMNS)
    values = [float(profile_row[column]) for column in DOMAIN_COLUMNS.values()]
    profile = str(profile_row["perfil"])
    fig = go.Figure(
        go.Bar(
            x=values,
            y=labels,
            orientation="h",
            marker_color=PROFILE_COLORS[profile],
            text=[f"{value:.2f}" for value in values],
            textposition="outside",
            hovertemplate="%{y}: %{x:.2f}<extra></extra>",
        )
    )
    fig.add_vline(x=0, line_color="#50606d", line_width=1.5)
    fig.update_layout(
        showlegend=False,
        xaxis_title="Puntaje estandarizado (0 = promedio departamental)",
        yaxis_title=None,
        xaxis=dict(range=[-2.4, 2.0], gridcolor="#edf1f3"),
        margin=dict(l=0, r=35, t=20, b=15),
        height=390,
    )
    return fig


def domain_comparison(
    municipality_row: pd.Series,
    profile_means: pd.Series,
) -> go.Figure:
    labels = list(DOMAIN_COLUMNS)
    municipality_values = [
        float(municipality_row[column]) for column in DOMAIN_COLUMNS.values()
    ]
    profile_values = [
        float(profile_means[column]) for column in DOMAIN_COLUMNS.values()
    ]
    frame = pd.DataFrame(
        {
            "Dimensión": labels * 2,
            "Puntaje": municipality_values + profile_values,
            "Referencia": ["Municipio"] * len(labels)
            + ["Promedio del perfil"] * len(labels),
        }
    )
    fig = px.bar(
        frame,
        x="Puntaje",
        y="Dimensión",
        color="Referencia",
        barmode="group",
        orientation="h",
        color_discrete_map={
            "Municipio": "#173b57",
            "Promedio del perfil": "#a6bcc3",
        },
    )
    fig.add_vline(x=0, line_color="#52616b", line_width=1)
    fig.update_layout(
        margin=dict(l=0, r=10, t=10, b=0),
        height=390,
        xaxis_title="Puntaje estandarizado",
        yaxis_title=None,
        legend_title_text=None,
    )
    return fig


def accessibility_scatter(
    data: pd.DataFrame,
    y_column: str,
    y_label: str,
) -> go.Figure:
    plot_data = data.copy()
    plot_data["perfil_texto"] = plot_data["perfil"].astype(str)
    fig = px.scatter(
        plot_data,
        x="distancia_lineal_nucleo_urbano_top5_km",
        y=y_column,
        color="perfil_texto",
        color_discrete_map=PROFILE_COLORS,
        category_orders={"perfil_texto": PROFILE_ORDER},
        hover_name="municipio",
        hover_data={
            "perfil_texto": False,
            "nodo_mas_cercano": True,
            "tramo_distancia": True,
        },
        labels={
            "distancia_lineal_nucleo_urbano_top5_km":
                "Distancia al nodo urbano más cercano (km)",
            y_column: y_label,
            "perfil_texto": "Perfil",
            "nodo_mas_cercano": "Nodo aproximado",
            "tramo_distancia": "Tramo",
        },
        opacity=0.78,
    )
    fig.update_traces(marker=dict(size=9, line=dict(width=0.4, color="white")))
    fig.update_layout(
        margin=dict(l=0, r=0, t=15, b=0),
        height=470,
        legend_title_text="Perfil",
    )
    return fig


def distance_domain_lines(data: pd.DataFrame) -> go.Figure:
    grouped = (
        data.assign(tramo_texto=data["tramo_distancia"].astype(str))
        .groupby("tramo_texto", observed=True)[list(DOMAIN_COLUMNS.values())]
        .median()
        .reindex(DISTANCE_ORDER)
        .reset_index()
    )
    long = grouped.melt(
        id_vars="tramo_texto",
        var_name="variable",
        value_name="Puntaje",
    )
    reverse_domains = {value: key for key, value in DOMAIN_COLUMNS.items()}
    long["Dimensión"] = long["variable"].map(reverse_domains)
    fig = px.line(
        long,
        x="tramo_texto",
        y="Puntaje",
        color="Dimensión",
        markers=True,
        category_orders={"tramo_texto": DISTANCE_ORDER},
        labels={"tramo_texto": "Distancia relativa"},
    )
    fig.add_hline(y=0, line_color="#7d8991", line_width=1)
    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        height=430,
        legend_title_text="Dimensión",
    )
    return fig


def sector_bar(row: pd.Series) -> go.Figure:
    frame = pd.DataFrame(
        {
            "Sector": list(SECTOR_COLUMNS),
            "Participación": [
                float(row[column]) for column in SECTOR_COLUMNS.values()
            ],
        }
    ).sort_values("Participación")
    fig = px.bar(
        frame,
        x="Participación",
        y="Sector",
        orientation="h",
        text_auto=".1f",
        color_discrete_sequence=["#356a85"],
    )
    fig.update_traces(
        texttemplate="%{x:.1f}%",
        textposition="outside",
        hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(l=0, r=25, t=10, b=0),
        height=390,
        xaxis_title="Participación CIIU (%)",
        yaxis_title=None,
    )
    return fig
