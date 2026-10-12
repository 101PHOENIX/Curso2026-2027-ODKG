# Hands-on assignment 4 – Self assessment

## Checklist

**Every RDF file:**

- [x] Uses the .ttl extension
- [x] Is serialized in the Turtle format
- [x] Follows the resource naming strategy
- [x] Uses class and property URIs that are the same as those used in the ontology

**Every URI in the RDF files:**

- [x] Is "readable" and has some meaning (e.g., it is not an auto-increased integer)
- [x] Is not encoded as a string
- [x] Does not contain a double slash (i.e., “//”)

**Every individual in the RDF files:**

- [x] Has a label with the name of the individual
- [x] Has a type

**Every value in the RDF files:**

- [x] Is trimmed
- [x] Is properly encoded (e.g., dates, booleans)
- [x] Includes its datatype
- [x] Uses the correct datatype (e.g., values of 0-1 may be booleans and not integers, not every string made of numbers is a number)

## Comments on the self-assessment

**Deliverables**

| File | Content |
|---|---|
| `mappings/madridnoise.rml` | Eight triples maps: stations, periods, observations, terraces, districts, neighbourhoods, datasets and Group03 agent |
| `mappings/madridnoise.yml` | Equivalent YARRRML rules (optional deliverable) |
| `rdf/madridnoise.ttl` | Generated RDF serialized in Turtle: **1,070,078 triples** |
| `rdf/queries.sparql` | Seventeen verification and application queries, executed individually against the data graph |

**How the RDF was generated**

First import the original municipal CSVs into OpenRefine **3.10.0**, apply the histories in `openrefine/`, and export the corresponding comma-separated UTF-8 `csv/*-updated.csv` files. Import/export handles the source encodings and CSV separators. The histories normalize value formats, identifiers and dates, repair station coordinate strings, select eligible terrace coordinate sources before conversion, and derive the percentile-order quality flag. The mappings use the resulting headers and values directly. The sources also include `csv/periods.csv` (four period labels) and `csv/datasets.csv` (three dataset metadata rows).

Run from the `Group03` directory with RMLMapper **7.3.3**:

```sh
java -jar rmlmapper.jar -m mappings/madridnoise.rml -s turtle -o rdf/madridnoise.ttl
```

[The ontology instance example](ontology/ontology-example.ttl) is an 86-triple subset of the generated graph. It illustrates station RF-02 and its day/night observations on **2025-01-01**, terrace 37, the four periods, geographic resources and dataset metadata.

**Scope and source limitations**

The graph contains 78,230 observations from **2025-01-01 to 2026-10-04**, all 31 stations and all 6,594 terraces, plus 21 districts, 129 neighbourhoods and four periods. The unchanged original noise CSV contains 295,853 observations from 2020 onwards; the chosen recent window removes 217,623 earlier observations. This is an application scope choice.

The terrace data remains a **4 October 2026 snapshot**. Using noise from 2025–2026 does not prove that the same terraces existed or operated on each noise date. The locations approximate premises/grouping entrances; the graph does not infer historical terrace activity or a causal effect on noise.

**Checklist notes**

- Individual IRIs follow `https://madridnoise.linkeddata.es/resource/<type>/<id>`. Observations use the readable station/date/period key. Terrace, district and neighbourhood IDs are official census codes, rather than generated counters. The `//` in `https://` is the required scheme separator; the check concerns accidental doubled path separators.
- Labels use Spanish source station/area names (`@es`) and descriptive English labels for observations, terraces and periods (`@en`). The three local dataset resources are typed `dcat:Dataset` and labelled; `agent:group03` is a labelled `dcterms:Agent` naming the creator/publisher of the RDF adaptations. External source/licence IRIs retain their provider identities.
- The three dataset descriptions provide titles, scope/processing descriptions, CC BY 4.0 licence links, source links, Group03 creator/publisher links and the adaptation modification date. Descriptions retain municipal attribution and the terrace snapshot limitation.
- Sound levels and coordinates use `xsd:decimal`, observation/metadata dates use `xsd:date`, terrace IDs use `xsd:integer`, and codes/names use `xsd:string`. Language-tagged labels use `rdf:langString`. All unavailable percentile values remain omitted: 17 observations have no percentile values.
- The `xsd:boolean` `mn:percentileOrderViolation` flag is true for 213 inconsistent complete sequences, false for 78,000 sequences satisfying the ordering check, and absent on the 17 incomplete sequences. Published numerical zeros remain source measurements; the flag makes anomalies visible without inventing replacements.
- The terrace location rule produces **6,534 located terraces and 60 without coordinates**. All terraces retain their types, labels, IDs and area links; unlocated terraces are excluded only from distance calculations.
- Validation: the Turtle parses, CSV-to-RDF checks match the source values, all eighteen local properties are used, and local resources have labels and types. All seventeen queries execute with Apache Jena against the data graph. Q2/Q3/Q4/Q5/Q11 return 0; Q6/Q13/Q15/Q17 return no violations; Q7 returns 17; Q14 returns 213 true, 78,000 false and 17 unavailable flags; Q16 returns 6,534 located and 60 unlocated terraces. Q12 includes all 31 stations, including RF-24=0, with RF-03=71, RF-04=55, RF-26=3 and RF-50=30.
- The optional YARRRML is checked against the RML rules; the RML file is the source used for RDF generation.
