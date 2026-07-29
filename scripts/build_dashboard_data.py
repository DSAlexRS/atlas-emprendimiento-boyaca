from __future__ import annotations

import json
import shutil
from pathlib import Path

import numpy as np
import pandas as pd


DASHBOARD = Path(__file__).resolve().parents[1]
PROJECT = DASHBOARD.parent
OUTPUT = DASHBOARD / "data"

BASE = (
    PROJECT
    / "data"
    / "intermediate"
    / "base_intermedia_emprendimiento_boyaca.csv"
)
CLUSTER_DIR = PROJECT / "outputs" / "clustering_municipal"
GEO = PROJECT / "data" / "raw" / "DANE_MGN2024_municipios_boyaca.geojson"


def exterior_rings(geometry: dict) -> list[list[list[float]]]:
    if geometry["type"] == "Polygon":
        return [geometry["coordinates"][0]]
    return [polygon[0] for polygon in geometry["coordinates"]]


def approximate_center(geometry: dict) -> tuple[float, float]:
    ring = max(exterior_rings(geometry), key=len)
    coordinates = np.asarray(ring, dtype=float)
    return float(coordinates[:, 0].mean()), float(coordinates[:, 1].mean())


def simplify_open_line(points: np.ndarray, tolerance: float) -> np.ndarray:
    if len(points) <= 2:
        return points
    keep = np.zeros(len(points), dtype=bool)
    keep[[0, -1]] = True
    stack = [(0, len(points) - 1)]
    while stack:
        start, end = stack.pop()
        segment = points[end] - points[start]
        candidates = points[start + 1:end]
        if not len(candidates):
            continue
        if np.allclose(segment, 0):
            distances = np.linalg.norm(candidates - points[start], axis=1)
        else:
            relative = candidates - points[start]
            distances = np.abs(
                segment[0] * relative[:, 1]
                - segment[1] * relative[:, 0]
            ) / np.linalg.norm(segment)
        position = int(np.argmax(distances))
        if distances[position] > tolerance:
            index = start + position + 1
            keep[index] = True
            stack.extend([(start, index), (index, end)])
    return points[keep]


def simplify_ring(
    ring: list[list[float]],
    tolerance: float = 0.0015,
) -> list[list[float]]:
    points = np.asarray(ring, dtype=float)
    if len(points) < 5:
        return [[round(x, 5), round(y, 5)] for x, y in points]
    core = points[:-1] if np.allclose(points[0], points[-1]) else points
    pivot = int(np.argmax(np.linalg.norm(core - core[0], axis=1)))
    first = simplify_open_line(core[:pivot + 1], tolerance)
    second = simplify_open_line(
        np.vstack([core[pivot:], core[0]]),
        tolerance,
    )
    simplified = np.vstack([first[:-1], second])
    if len(simplified) < 4:
        simplified = np.vstack([core[:3], core[0]])
    return [[round(x, 5), round(y, 5)] for x, y in simplified]


def signed_ring_area(ring: list[list[float]]) -> float:
    return 0.5 * sum(
        ring[index][0] * ring[index + 1][1]
        - ring[index + 1][0] * ring[index][1]
        for index in range(len(ring) - 1)
    )


def orient_ring(
    ring: list[list[float]],
    *,
    clockwise: bool,
) -> list[list[float]]:
    area = signed_ring_area(ring)
    if (clockwise and area > 0) or (not clockwise and area < 0):
        return list(reversed(ring))
    return ring


def simplify_polygon(polygon: list[list[list[float]]]) -> list[list[list[float]]]:
    simplified = []
    for index, ring in enumerate(polygon):
        simplified_ring = simplify_ring(ring)
        simplified.append(
            orient_ring(simplified_ring, clockwise=index == 0)
        )
    return simplified


def simplify_geometry(geometry: dict) -> dict:
    if geometry["type"] == "Polygon":
        coordinates = simplify_polygon(geometry["coordinates"])
    else:
        coordinates = [
            simplify_polygon(polygon)
            for polygon in geometry["coordinates"]
        ]
    return {"type": geometry["type"], "coordinates": coordinates}


def haversine_km(
    lat1: float,
    lon1: float,
    lat2: np.ndarray,
    lon2: np.ndarray,
) -> np.ndarray:
    radius = 6371.0088
    lat1, lon1 = np.radians([lat1, lon1])
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    )
    return 2 * radius * np.arcsin(np.sqrt(a))


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)

    base = pd.read_csv(
        BASE,
        dtype={"codigo_municipio": str, "codigo_departamento": str},
    )
    clusters = pd.read_csv(
        CLUSTER_DIR / "clusters_municipales_boyaca.csv",
        dtype={"codigo_municipio": str},
    )
    scores = pd.read_csv(
        CLUSTER_DIR / "puntajes_municipales_dominios.csv",
        dtype={"codigo_municipio": str},
    )
    poles = pd.read_csv(
        CLUSTER_DIR / "polos_secundarios_exploratorios.csv",
        dtype={"codigo_municipio": str},
    )

    digital_columns = [
        "pct_reporta_billetera_digital_si",
        "pct_reporta_pago_tarjeta_si",
        "pct_reporta_pago_qr_si",
        "pct_reporta_transferencia_ach_si",
    ]
    base["promedio_reporte_medios_digitales"] = base[
        digital_columns
    ].mean(axis=1)

    data = (
        base.merge(
            clusters,
            on=["codigo_municipio", "municipio"],
            how="inner",
            validate="one_to_one",
        )
        .merge(
            scores,
            on=["codigo_municipio", "municipio"],
            how="inner",
            validate="one_to_one",
        )
    )

    geo = json.loads(GEO.read_text(encoding="utf-8"))
    feature_by_code = {
        feature["properties"]["MPIO_CDPMP"]: feature
        for feature in geo["features"]
    }
    centers = {
        code: approximate_center(feature["geometry"])
        for code, feature in feature_by_code.items()
    }

    nodes = data.nlargest(5, "poblacion_cabecera_2023")[
        ["codigo_municipio", "municipio", "poblacion_cabecera_2023"]
    ].copy()
    nodes["longitude"] = nodes["codigo_municipio"].map(
        lambda code: centers[code][0]
    )
    nodes["latitude"] = nodes["codigo_municipio"].map(
        lambda code: centers[code][1]
    )

    nearest_nodes = []
    for row in data.itertuples(index=False):
        longitude, latitude = centers[row.codigo_municipio]
        distances = haversine_km(
            latitude,
            longitude,
            nodes["latitude"].to_numpy(),
            nodes["longitude"].to_numpy(),
        )
        nearest_nodes.append(nodes.iloc[int(np.argmin(distances))]["municipio"])
    data["nodo_mas_cercano"] = nearest_nodes
    data["tramo_distancia"] = pd.qcut(
        data["distancia_lineal_nucleo_urbano_top5_km"],
        q=5,
        labels=[
            "Muy próximo",
            "Próximo",
            "Intermedio",
            "Lejano",
            "Muy lejano",
        ],
    ).astype(str)
    data["candidato_polo_secundario"] = data["codigo_municipio"].isin(
        set(poles["codigo_municipio"])
    )

    selected_columns = [
        "codigo_municipio",
        "municipio",
        "n_unidades_economicas_urbanas",
        "flag_universo_analitico_menor_30",
        "poblacion_total_2023",
        "poblacion_cabecera_2023",
        "pct_poblacion_cabecera_2023",
        "area_municipal_km2",
        "densidad_poblacion_hab_km2_2023",
        "ue_urbanas_visibles_por_1000_hab_total_2023",
        "va_total_2023_miles_millones_cop",
        "va_2023_por_habitante_millones_cop",
        "distancia_lineal_nucleo_urbano_top5_km",
        "nodo_mas_cercano",
        "tramo_distancia",
        "cluster",
        "perfil",
        "silueta_individual",
        "distancia_centroide",
        "margen_pertenencia",
        "tipo_asignacion",
        "region_contigua",
        "candidato_polo_secundario",
        "madurez_permanencia_observada",
        "formalizacion_gestion",
        "escala_capacidades",
        "finanzas_redes",
        "densidad_emprendedora",
        "pct_operacion_menos_3_anios",
        "pct_operacion_mas_10_anios",
        "pct_persona_natural",
        "pct_rut_si",
        "pct_no_lleva_registros_contables",
        "pct_ue_un_solo_trabajador_sociodemografico",
        "pct_ue_ingresos_hasta_10m_2023",
        "pct_propietarios_educacion_superior",
        "promedio_reporte_medios_digitales",
        "pct_solicito_credito_si",
        "pct_asociacion_productores_comerciantes_si",
        "pct_ciiu_primario_extractivo_sectorial_2023",
        "pct_ciiu_manufactura_sectorial_2023",
        "pct_ciiu_infraestructura_logistica_sectorial_2023",
        "pct_ciiu_comercio_sectorial_2023",
        "pct_ue_alojamiento_comidas_sectorial_2023",
        "pct_ciiu_servicios_empresariales_conocimiento_sectorial_2023",
        "pct_ciiu_servicios_sociales_personales_sectorial_2023",
    ]
    dashboard_data = data[selected_columns].sort_values(
        "codigo_municipio"
    )

    assert dashboard_data.shape == (123, len(selected_columns))
    assert dashboard_data["codigo_municipio"].is_unique
    assert dashboard_data[selected_columns].isna().sum().sum() == 0
    assert dashboard_data["perfil"].nunique() == 5
    assert dashboard_data["tramo_distancia"].nunique() == 5

    dashboard_data.to_csv(
        OUTPUT / "municipios_dashboard.csv",
        index=False,
        encoding="utf-8-sig",
    )

    curated_geo = {
        "type": "FeatureCollection",
        "name": "municipios_boyaca",
        "crs": geo.get("crs"),
        "features": [],
    }
    names = dashboard_data.set_index("codigo_municipio")["municipio"].to_dict()
    for feature in geo["features"]:
        code = feature["properties"]["MPIO_CDPMP"]
        simplified_geometry = simplify_geometry(feature["geometry"])
        assert all(
            signed_ring_area(ring) < 0
            for ring in exterior_rings(simplified_geometry)
        ), f"Orientación cartográfica inválida para {code}"
        curated_geo["features"].append(
            {
                "type": "Feature",
                "properties": {
                    "codigo_municipio": code,
                    "municipio": names[code],
                },
                "geometry": simplified_geometry,
            }
        )
    (OUTPUT / "municipios_boyaca.geojson").write_text(
        json.dumps(curated_geo, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )

    copies = {
        "asociaciones_distancia_accesibilidad.csv":
            "asociaciones_distancia.csv",
        "autocorrelacion_espacial_dominios.csv":
            "autocorrelacion_espacial.csv",
        "resumen_coincidencia_espacial.csv":
            "resumen_espacial.csv",
    }
    for source, target in copies.items():
        shutil.copyfile(CLUSTER_DIR / source, OUTPUT / target)

    print(
        {
            "rows": len(dashboard_data),
            "columns": len(dashboard_data.columns),
            "profiles": dashboard_data["perfil"].nunique(),
            "distance_bands": dashboard_data["tramo_distancia"].nunique(),
            "candidate_poles": int(
                dashboard_data["candidato_polo_secundario"].sum()
            ),
            "output": str(OUTPUT),
        }
    )


if __name__ == "__main__":
    main()
