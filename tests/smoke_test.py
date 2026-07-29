from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

APP = Path(__file__).resolve().parents[1] / "app.py"
DATA_DIR = APP.parent / "data"

from streamlit.testing.v1 import AppTest


PAGES = [
    "Panorama territorial",
    "Perfiles municipales",
    "Accesibilidad y espacio",
    "Ficha municipal",
    "Método y alcance",
]


def signed_ring_area(ring: list[list[float]]) -> float:
    return 0.5 * sum(
        ring[index][0] * ring[index + 1][1]
        - ring[index + 1][0] * ring[index][1]
        for index in range(len(ring) - 1)
    )


def exterior_rings(geometry: dict) -> list[list[list[float]]]:
    if geometry["type"] == "Polygon":
        return [geometry["coordinates"][0]]
    return [polygon[0] for polygon in geometry["coordinates"]]


def main() -> None:
    data = pd.read_csv(
        DATA_DIR / "municipios_dashboard.csv",
        dtype={"codigo_municipio": str},
    )
    geojson = json.loads(
        (DATA_DIR / "municipios_boyaca.geojson").read_text(encoding="utf-8")
    )
    data_codes = set(data["codigo_municipio"])
    geometry_codes = {
        feature["properties"]["codigo_municipio"]
        for feature in geojson["features"]
    }
    assert data.shape[0] == 123
    assert data["codigo_municipio"].is_unique
    assert data["perfil"].nunique() == 5
    assert data["tramo_distancia"].nunique() == 5
    assert data.isna().sum().sum() == 0
    assert data_codes == geometry_codes
    assert all(
        signed_ring_area(ring) < 0
        for feature in geojson["features"]
        for ring in exterior_rings(feature["geometry"])
    )

    app = AppTest.from_file(str(APP), default_timeout=30)
    app.run()
    assert not app.exception, app.exception

    results = {}
    for page in PAGES:
        app.radio[0].set_value(page).run()
        assert not app.exception, f"{page}: {app.exception}"
        results[page] = {
            "titles": len(app.title),
            "metrics": len(app.metric),
            "dataframes": len(app.dataframe),
            "plotly_charts": len(app.get("plotly_chart")),
        }
    print({"status": "OK", "pages": results})


if __name__ == "__main__":
    main()
