# Hands-on assignment 3 – Self assessment

## Checklist

**Every resource described in the CSV file:**

- [x] Has a unique identifier in a column (not an auto-increased integer)
- [x] Is related to a class in the ontology

**Every class in the ontology:**

- [x] Is related to a resource described in the CSV file

**Every column in the CSV file:**

- [x] Is trimmed
- [x] Is properly encoded (e.g., dates, booleans)
- [x] Is related to a property in the ontology

**Every property in the ontology:**

- [x] Is related to a column in the CSV file

## Comments on the self-assessment

**Deliverables and reproduction**

| Source file (`csv/`) | OpenRefine operations (`openrefine/`) | Updated file (`csv/`) | Rows |
|---|---|---|---|
| `contaminacion_acustica.csv` | `contaminacion_acustica.json` (24 operations) | `contaminacion_acustica-updated.csv` | 78,230 |
| `estaciones_acusticas.csv` | `estaciones_acusticas.json` (9 operations) | `estaciones_acusticas-updated.csv` | 31 |
| `terrazas_hosteleria.csv` | `terrazas_hosteleria.json` (15 operations) | `terrazas_hosteleria-updated.csv` | 6,594 |

The updated CSVs were produced with OpenRefine **3.10.0** using these histories. Import the originals with semicolon separator, one header row, disabled cell type guessing, and blank cells stored as nulls. Use ISO-8859-1 for noise/stations and UTF-8 for terraces; OpenRefine handles the terrace BOM. Apply the matching JSON through *Undo / Redo → Apply*, remove active facets, and export comma-separated UTF-8 CSV. Fresh imports and complete history replays reproduced every field and row order of the updated CSVs. Import settings are not stored in the history JSON.

**Daily noise (`contaminacion_acustica`)**

- The original 2020–2026 source extract contains 295,853 rows. Cleaning selects 78,230 observations from 2025-01-01 to 2026-10-04, removing 217,623 earlier rows as a chosen recent application window. This selection does not establish that the 2026 terrace snapshot is contemporaneous with the noise measurements.
- `Estación` 2 becomes `RF-02`, with two-digit padding; all 31 measurement codes join the station catalogue. `Año`/`Mes`/`Día` become the ISO `date`, validated with `toDate`; `period` is trimmed and upper-cased.
- Decimal commas in `LAeq`, `L1`…`L99` become dots. `N/D` becomes an empty cell on 17 rows. Reported numerical zeros and other suspect measurements are retained rather than replaced.
- The derived `percentile_order_violation` column is `true` for 213 complete rows violating `L1 >= L10 >= L50 >= L90 >= L99`, `false` for 78,000 complete rows satisfying that check, and blank for 17 rows with unavailable percentiles. It maps to `mn:percentileOrderViolation` as `xsd:boolean`. A false flag confirms this check only, not every aspect of measurement quality. For example, `RF-20-2025-04-28-D` retains its published L10 of 0 and has a true flag.
- The derived `observation_id` (`RF-02-2025-01-01-N`) uses the canonical station/date/period key. All 78,230 identifiers are unique. The updated CSV has 11 columns, including the quality flag.

**Stations (`estaciones_acusticas`)**

- Codes and names are trimmed, with internal spaces collapsed.
- `40.409.121` becomes `40.409121`, and `-3.691.509` becomes `-3.691509`. Repaired geographic values were checked against the station's ETRS89 X/Y.
- The updated CSV keeps four columns: code, name, latitude and longitude.

**Terraces (`terrazas_hosteleria`)**

- Access type, premises status, local X/Y and grouping X/Y are retained until coordinate selection is complete. Street-access premises (`id_tipo_acceso_local=1`) not in Baja (status 8/9) use local coordinates; grouped premises (access type 0) use grouping coordinates. Other access types and missing/zero pairs have no usable location.
- A Jython inverse transverse-Mercator expression converts the selected ETRS89 / UTM 30N (EPSG:25830) point to WGS84 latitude/longitude. There are 6,443 located street-access terraces and 91 located grouped terraces: **6,534 located, 60 unlocated**. All 6,594 terrace identifiers and geographic links are kept. Premises/grouping entrances are location proxies, not surveyed terrace centroids.
- Source IDs are written as plain integers; padded district/neighbourhood names are trimmed. Each of the 21 district IDs and 129 neighbourhood IDs has one consistent label.
- The eight output columns are `terrace_id`, `terrace_label`, `district_id`, `district_label`, `neighbourhood_id`, `neighbourhood_label`, `latitude`, `longitude`. `terrace_label` is derived as `Terrace 37`, for example; helper source columns are dropped after conversion.

**Checklist notes**

- Identifiers are source codes or composite source keys, not generated row counters. `observation_id` is a URI helper; other retained values map to ontology properties or `rdfs:label`.
- The six local application classes and eighteen local properties are covered by the cleaned data. The property count includes the derived quality flag.
- `mn:DayPeriod` is represented by `period`; the four labels come from `csv/periods.csv`. `csv/datasets.csv` is a three-row reference table describing the generated datasets and Group03 creator/publisher for assignment 4.
