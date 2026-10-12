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

**Deliverables**

| Source file (`csv/`) | OpenRefine operations (`openrefine/`) | Updated file (`csv/`) | Rows |
|---|---|---|---|
| `contaminacion_acustica.csv` | `contaminacion_acustica.json` (23 operations) | `contaminacion_acustica-updated.csv` | 78,230 |
| `estaciones_acusticas.csv` | `estaciones_acusticas.json` (9 operations) | `estaciones_acusticas-updated.csv` | 31 |
| `terrazas_hosteleria.csv` | `terrazas_hosteleria.json` (15 operations) | `terrazas_hosteleria-updated.csv` | 6,594 |

The JSON files are the operation histories extracted from OpenRefine 3.10.1. Each project was imported with `;` as separator, no cell type guessing, and encoding ISO-8859-1 (noise and stations) or UTF-8 (terraces). To reproduce, import the source file with those options and apply the JSON with *Undo / Redo → Apply*. The cleaning follows the rules in `analysis.html`.

**Daily noise (`contaminacion_acustica`)**
- Rows before 2025 are removed. The committed 2020–2026 extract would give ~3.3 M triples (~160 MB of Turtle), above GitHub's 100 MB limit, and 2025 onwards matches the 2026 terrace-census snapshot.
- `Estación` 2 → `RF-02` (padded to two digits) so it joins the station catalog. All 31 codes match.
- `Año`/`Mes`/`Día` → one ISO date (`2025-01-01`), validated with `toDate`.
- `Periodo` trimmed and upper-cased (D/E/N/T).
- `LAeq`, `L1`…`L99`: decimal comma → dot. `N/D` → empty cell (17 rows), never 0.
- New `observation_id` column (`RF-02-2025-01-01-N`) as the unique, readable key. Columns renamed to ASCII names.

**Stations (`estaciones_acusticas`)**
- Code and name trimmed, with internal spaces collapsed.
- `LATITUD`/`LONGITUD` repaired: `40.409.121` → `40.409121`, `-3.691.509` → `-3.691509`. The values were checked against each station's ETRS89 X/Y.

**Terraces (`terrazas_hosteleria`)**
- Only the 7 source columns the ontology uses are kept, out of 117.
- `id_terraza`, `id_distrito_local` and `id_barrio_local` are written as plain integers.
- District and neighbourhood names trimmed: the padded `"VILLA DE VALLECAS   "` becomes `VILLA DE VALLECAS`.
- Premises coordinates converted from ETRS89 / UTM 30N (EPSG:25830) to WGS84 latitude/longitude with a Jython expression (inverse transverse Mercator). 112 terraces with zero or unusable coordinates are left empty.
- New `terrace_label` column (`Terrace 37`).

**Checklist notes**
- Identifiers are source codes, not counters we generated: the RF station code, the station/date/period key for observations, and the census `id_terraza`, `id_distrito_local` and `id_barrio_local`.
- `mn:DayPeriod` is covered by the noise `period` column. Its labels come from the small reference table `csv/periods.csv`.
- Every remaining column maps to an ontology property or to `rdfs:label` (see `mappings/madridnoise.rml`).
