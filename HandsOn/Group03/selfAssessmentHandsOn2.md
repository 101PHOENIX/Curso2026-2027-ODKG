# Hands-on assignment 2 – Self assessment

## Checklist

**The “analysis.html” file:**

- [x] Includes the potential license of the dataset to be generated
- [x] Includes the resource naming strategy

**The resource naming strategy:**

- [x] Uses a domain that is not the one given by default in Protégé
- [x] Uses different paths for ontology resources (i.e., classes and properties) and individuals
- [x] Ensures that the paths for individuals of different classes are not the same
- [x] Defines individual URIs independently of class URIs

**The ontology file:**

- [x] Uses the .ttl extension
- [x] Is serialized in the Turtle format
- [x] Follows the resource naming strategy
- [x] Contains at least one class
- [x] Contains at least one object property (where the value of the property is a resource)
- [x] Contains at least one datatype property (where the value of the property is a string literal, usually typed)
- [x] Defines the domain of all the properties (the origin of the property)
- [x] Defines the range of all the properties (the destination of the property)
- [x] Defines all class names starting with a capital letter
- [x] Defines all property names starting with a non-capital letter
- [x] Does not mix labels in different languages (e.g., Spanish and English)
- [x] Does not define multiple domains or multiple ranges in properties
- [x] Contains at least one class that will be used to link to other entities

## Comments on the self-assessment

The final ontology contains 6 local classes and 18 local properties: 4 object properties and 14 datatype properties. Each local property has one explicit domain and one range. The boolean `mn:percentileOrderViolation` records whether a complete noise-percentile sequence violates its expected order; it preserves the source measurements and remains absent when a percentile is unavailable. Ontology version 1.1 is dated 2026-10-12.

The resource naming strategy uses `https://madridnoise.linkeddata.es/ontology#` for classes and properties, separate `/resource/<type>/<id>` paths for individuals, and `/dataset/<name>` for the generated datasets. The generated-data creator and publisher is the labelled agent `/resource/agent/group03`. Existing vocabularies supply dataset and agent metadata; their terms retain their external definitions.

`ontology/ontology-example.ttl` is an exact subset of the generated `rdf/madridnoise.ttl` graph. It includes station RF-02, its actual day and night observations on 2025-01-01 with their source measurements and boolean quality flags, all four periods, terrace 37, district 18 and neighbourhood 1801. It also includes the three generated datasets and the Group03 agent with the implemented source, licence, creator/publisher and date metadata. All example individuals have types and labels, and all instance triples are present in the delivered graph.

The generated noise dataset covers 2025-01-01 through 2026-10-04; the terrace data is a census snapshot loaded on 2026-10-04, and the station extract's source snapshot date is unspecified. Metadata distinguishes these scopes and records 2026-10-12 as the generated datasets' modification date.
