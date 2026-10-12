"""Prepare the Group03 source CSVs for the RML mappings.

Reads the three portal files in ../csv/ and writes UTF-8, comma-separated,
mapping-ready files to ../csv/clean/, applying the normalisation rules
documented in analysis.html:

* noise: ISO-8859-1 -> UTF-8, decimal comma -> dot, N/D -> empty (omitted),
  station number -> RF-NN code, Año/Mes/Día -> YYYY-MM-DD.
* stations: trimmed names, repaired WGS84 strings (-3.691.509 -> -3.691509),
  checked against the station's own ETRS89/UTM X/Y.
* terraces: id_terraza without leading zeros, trimmed district/neighbourhood
  labels, premises ETRS89 / UTM 30N (EPSG:25830) -> WGS84 (EPSG:4326);
  zero/unusable coordinates are left empty.

Usage:  python3 preprocess.py [--since YYYY-MM-DD]

--since limits the noise observations that are mapped (default 2025-01-01).
The committed csv/contaminacion_acustica.csv covers 2020-01-01 to 2026-10-04;
mapping all of it yields ~3.3 M triples (~160 MB of Turtle), above GitHub's
100 MB file limit. 2025 onwards matches the 2026 terrace-census snapshot the
noise is compared with. Use --since 2020-01-01 to transform the whole extract.
Only the Python standard library and pandas are needed.
"""
import math
import os
import re
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "csv")
OUT = os.path.join(SRC, "clean")


# --- ETRS89 / UTM zone 30N -> geographic (GRS80 ~ WGS84 at cm level) -------
# Inverse transverse Mercator with Krüger's series (accurate to < 1 mm).
_A = 6378137.0
_F = 1 / 298.257222101
_K0 = 0.9996
_N = _F / (2 - _F)
_AA = _A / (1 + _N) * (1 + _N**2 / 4 + _N**4 / 64)
_BETA = [
    _N / 2 - 2 * _N**2 / 3 + 37 * _N**3 / 96,
    _N**2 / 48 + _N**3 / 15,
    17 * _N**3 / 480,
]
_DELTA = [
    2 * _N - 2 * _N**2 / 3 - 2 * _N**3,
    7 * _N**2 / 3 - 8 * _N**3 / 5,
    56 * _N**3 / 15,
]


def utm_to_wgs84(x, y, zone=30):
    xi = y / (_K0 * _AA)
    eta = (x - 500000.0) / (_K0 * _AA)
    xi_p, eta_p = xi, eta
    for j, b in enumerate(_BETA, start=1):
        xi_p -= b * math.sin(2 * j * xi) * math.cosh(2 * j * eta)
        eta_p -= b * math.cos(2 * j * xi) * math.sinh(2 * j * eta)
    chi = math.asin(math.sin(xi_p) / math.cosh(eta_p))
    lat = chi
    for j, d in enumerate(_DELTA, start=1):
        lat += d * math.sin(2 * j * chi)
    lon0 = math.radians((zone - 1) * 6 - 180 + 3)
    lon = lon0 + math.atan2(math.sinh(eta_p), math.cos(xi_p))
    return math.degrees(lat), math.degrees(lon)


def fix_geo(value):
    """'-3.691.509' -> '-3.691509': keep sign and first dot, join the rest."""
    value = value.strip()
    m = re.fullmatch(r"(-?\d+)\.(\d+)(?:\.(\d+))*", value)
    if not m:
        raise ValueError(f"unexpected coordinate format: {value!r}")
    head, rest = value.split(".", 1)
    return f"{head}.{rest.replace('.', '')}"


def decimal(value):
    value = str(value).strip()
    if value in ("", "N/D", "nan"):
        return ""
    return f"{float(value.replace(',', '.')):.1f}"


def stations():
    df = pd.read_csv(os.path.join(SRC, "estaciones_acusticas.csv"), sep=";",
                     encoding="latin-1", dtype=str)
    rows = []
    for _, r in df.iterrows():
        lat, lon = float(fix_geo(r["LATITUD"])), float(fix_geo(r["LONGITUD"]))
        clat, clon = utm_to_wgs84(float(r["X"]), float(r["Y"]))
        # repaired string must agree with the projected pair (~< 150 m)
        if abs(lat - clat) > 0.002 or abs(lon - clon) > 0.002:
            sys.exit(f"coordinate check failed for {r['ESTACIÓN']}")
        rows.append({
            "station_code": r["ESTACIÓN"].strip(),
            "station_name": " ".join(r["NOMBRE"].split()),
            "latitude": f"{lat:.6f}",
            "longitude": f"{lon:.6f}",
        })
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(OUT, "stations.csv"), index=False)
    return set(out["station_code"])


def noise(known_stations, since):
    df = pd.read_csv(os.path.join(SRC, "contaminacion_acustica.csv"), sep=";",
                     encoding="latin-1", dtype=str)
    df.columns = ["station", "year", "month", "day", "period",
                  "LAeq", "L1", "L10", "L50", "L90", "L99"]
    code = "RF-" + df["station"].str.strip().astype(int).map(lambda n: f"{n:02d}")
    date = pd.to_datetime(dict(year=df["year"].astype(int),
                               month=df["month"].astype(int),
                               day=df["day"].astype(int))).dt.strftime("%Y-%m-%d")
    period = df["period"].str.strip().str.upper()
    unknown = set(code) - known_stations
    if unknown:
        sys.exit(f"stations missing from catalog: {sorted(unknown)}")
    if not set(period) <= {"D", "E", "N", "T"}:
        sys.exit(f"unexpected periods: {set(period)}")
    out = pd.DataFrame({
        "observation_id": code + "-" + date + "-" + period,
        "station_code": code,
        "date": date,
        "period": period,
        "laeq": df["LAeq"].map(decimal),
        "l1": df["L1"].map(decimal),
        "l10": df["L10"].map(decimal),
        "l50": df["L50"].map(decimal),
        "l90": df["L90"].map(decimal),
        "l99": df["L99"].map(decimal),
    })
    assert out["observation_id"].is_unique
    out = out[out["date"] >= since]
    out.to_csv(os.path.join(OUT, "noise_observations.csv"), index=False)


def periods():
    pd.DataFrame([
        ("D", "Day (07:00-19:00)"),
        ("E", "Evening (19:00-23:00)"),
        ("N", "Night (23:00-07:00)"),
        ("T", "Total (24h)"),
    ], columns=["period", "label"]).to_csv(
        os.path.join(OUT, "periods.csv"), index=False)


def terraces():
    df = pd.read_csv(os.path.join(SRC, "terrazas_hosteleria.csv"), sep=";",
                     encoding="utf-8-sig", dtype=str, keep_default_na=False)
    rows = []
    for _, r in df.iterrows():
        x = float(r["coordenada_x_local"] or 0)
        y = float(r["coordenada_y_local"] or 0)
        lat = lon = ""
        if x > 0 and y > 0:
            la, lo = utm_to_wgs84(x, y)
            if 40.2 < la < 40.7 and -4.0 < lo < -3.4:  # Madrid bounds
                lat, lon = f"{la:.9f}", f"{lo:.9f}"
        tid = int(r["id_terraza"])
        rows.append({
            "terrace_id": tid,
            "terrace_label": f"Terrace {tid}",
            "district_id": int(r["id_distrito_local"]),
            "district_label": " ".join(r["desc_distrito_local"].split()),
            "neighbourhood_id": int(r["id_barrio_local"]),
            "neighbourhood_label": " ".join(r["desc_barrio_local"].split()),
            "latitude": lat,
            "longitude": lon,
        })
    out = pd.DataFrame(rows)
    assert out["terrace_id"].is_unique
    out.to_csv(os.path.join(OUT, "terraces.csv"), index=False)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="2025-01-01")
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    noise(stations(), args.since)
    periods()
    terraces()
    print("clean CSVs written to", os.path.normpath(OUT))
