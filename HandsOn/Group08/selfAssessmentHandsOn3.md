# Self-assessment Hands-On 3 (OpenRefine) - Group08

## Checklist

- [x] Data imported into OpenRefine (D1, D2, D3)
- [x] Data analysed and errors from the previous hands-on fixed
- [x] Data transformed to facilitate RDF generation
- [x] JSON operation history for every dataset under `openrefine/`
- [x] Updated CSV for every dataset under `csv/` (`*-updated.csv`)
- [x] JSON histories reproduce the CSVs (single-cell edits replaced by GREL transforms)
- [x] Self-assessment file in the root of the group directory

## Comments

**D1 - Climate shelters (`xarxa-refugis-climatics`, 550 rows)**
- Trimmed whitespace and collapsed double spaces; converted numbers. `created`/`modified` keep the source's local time as `YYYY-MM-DDTHH:MM:SS` (no UTC shift).
- Fixed name typos via clustering.
- `register_id` contains digits only and is unique.
- HTML timetable converted to plain text; HTML tags stripped from `values_value`.
- Abbreviated street names (C, Av, Pl, Pg) expanded to the full official form.
- Category derived from the name and mapped to English (Library, SwimmingPool, SportsCentre, Park, School, Museum, HealthCentre, Market, CivicCentre, WaterPlayArea, Other).
- Canonical district names.
- Extracted `email`, `website` and `telephone` columns; non-URL notes removed from `website`.

**D2 - Drinking fountains (`fonts-beure-2026`, 1760 rows)**
- Fixed wrong district codes (18->03, 19->04, 29->06, 37->07).
- Canonical district names.
- Filled the missing neighbourhood of 10 fountains using the official codes.
- `CARRER` normalised to ALL CAPS with undotted prefixes (C, AV, PL, PG, ...); typos fixed; `NOM` case variants unified; `SN` street numbers blanked.

**D3 - Street trees (`arbrat_viari`, 145,034 rows)**
- Cleaned by a teammate and validated by re-applying the JSON history.
- District and neighbourhood names aligned with the official codes, so they match D1 and D2.
- Appended ops: `-` placeholders blanked in the species-name columns, `espai_verd` spacing and case unified, missing neighbourhood filled for 7 trees from the nearest tree on the same street.

**Reproducibility:** all manual single-cell edits were replaced by GREL transforms, so applying each `openrefine/*.json` to the original data reproduces the corresponding `csv/*-updated.csv`.
