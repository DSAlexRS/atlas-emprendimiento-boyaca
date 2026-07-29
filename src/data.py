from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

from .content import DISTANCE_ORDER, PROFILE_ORDER


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    data = pd.read_csv(
        DATA_DIR / "municipios_dashboard.csv",
        dtype={"codigo_municipio": str},
    )
    data["perfil"] = pd.Categorical(
        data["perfil"], categories=PROFILE_ORDER, ordered=True
    )
    data["tramo_distancia"] = pd.Categorical(
        data["tramo_distancia"], categories=DISTANCE_ORDER, ordered=True
    )
    return data


@st.cache_data(show_spinner=False)
def load_geojson() -> dict:
    return json.loads(
        (DATA_DIR / "municipios_boyaca.geojson").read_text(encoding="utf-8")
    )


@st.cache_data(show_spinner=False)
def load_associations() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "asociaciones_distancia.csv")


@st.cache_data(show_spinner=False)
def load_moran() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "autocorrelacion_espacial.csv")


@st.cache_data(show_spinner=False)
def load_spatial_summary() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "resumen_espacial.csv")


def apply_filters(
    data: pd.DataFrame,
    profiles: list[str],
    distance_bands: list[str],
) -> pd.DataFrame:
    mask = data["perfil"].astype(str).isin(profiles)
    mask &= data["tramo_distancia"].astype(str).isin(distance_bands)
    return data.loc[mask].copy()


def fmt_integer(value: float | int) -> str:
    return f"{int(round(value)):,.0f}".replace(",", ".")


def fmt_decimal(value: float, digits: int = 1) -> str:
    return f"{value:,.{digits}f}".replace(",", "X").replace(".", ",").replace("X", ".")

