# Group03 — Terraces and night-time noise in Madrid

The project combines Madrid's daily noise measurements, acoustic station catalogue and registered hospitality terraces to explore terrace counts near stations and night-time LAeq.

The RDF contains **78,230 observations from 2025-01-01 to 2026-10-04**, 31 stations and 6,594 terraces. Of the terraces, 6,534 have usable approximate locations and 60 remain unlocated. The terrace inventory is a **4 October 2026 snapshot**; it does not establish historical terrace activity on each noise date.

## Deliverables

| Work | Files |
|---|---|
| Requirements and analysis | [Dataset requirements](requirements/datasetRequirements.html), [application requirements](requirements/applicationRequirements.html), [data analysis and naming strategy](analysis.html) |
| Ontology | [Ontology](ontology/ontology.ttl), [instance example](ontology/ontology-example.ttl), [HO2 self-assessment](selfAssessmentHandsOn2.md) |
| HO3 data preparation | [Original and updated CSVs](csv/), [OpenRefine histories](openrefine/), [self-assessment](selfAssessmentHandsOn3.md) |
| HO4 transformation | [RML](mappings/madridnoise.rml), [optional YARRRML](mappings/madridnoise.yml), [Turtle data](rdf/madridnoise.ttl), [SPARQL queries](rdf/queries.sparql), [self-assessment](selfAssessmentHandsOn4.md) |
| Reference tables | [Period labels](csv/periods.csv), [dataset metadata](csv/datasets.csv) |

## Reproduce the data

1. Import the three original CSVs into **OpenRefine 3.10.0** with semicolon separators, one header row, disabled cell type guessing and blank cells stored as nulls. Use ISO-8859-1 for noise/stations and UTF-8 for terraces. The [HO3 self-assessment](selfAssessmentHandsOn3.md) records the file-specific preparation rules.
2. Apply each matching `openrefine/*.json` history, remove active facets, and export comma-separated UTF-8 CSV to the matching `csv/*-updated.csv` path.
3. Run **RMLMapper 7.3.3** from `HandsOn/Group03/`, using the engine JAR as `rmlmapper.jar` in the command below (adjust its path to your installation):

   ```sh
   java -jar rmlmapper.jar -m mappings/madridnoise.rml -s turtle -o rdf/madridnoise.ttl
   ```

4. Load `rdf/madridnoise.ttl` into a SPARQL engine and execute the seventeen queries in [queries.sparql](rdf/queries.sparql) individually against the data graph. The generated graph contains **1,070,078 triples**; expected validation results are recorded in the query comments and [HO4 self-assessment](selfAssessmentHandsOn4.md).

The original noise CSV preserves the 295,853-row 2020–2026 source extract. Its OpenRefine history selects the 2025–2026 application window. Published sound levels are preserved; a boolean quality flag marks 213 complete percentile sequences with inconsistent ordering.

## Members

- Diego Aquino (@diegoaquinoh) **Leader**
- Sebastian Linares (@sebasl10)
- Noah Rose (@nsr223)
- Pedro López-Ríos (@plopezriosdc)
- Sergio Gismera Pino (@SergioGismeraPino)
