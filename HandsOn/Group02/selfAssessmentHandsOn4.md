# Hands-on assignment 4 – Self assessment

## Checklist

**Every RDF file:**

- [X] Uses the .ttl extension
- [X] Is serialized in the Turtle format
- [X] Follows the resource naming strategy
- [X] Uses class and property URIs that are the same as those used in the ontology

**Every URI in the RDF files:**

- [ ] Is "readable" and has some meaning (e.g., it is not an auto-increased integer)
- [X] Is not encoded as a string
- [X] Does not contain a double slash (i.e., “//”)

**Every individual in the RDF files:**

- [X] Has a label with the name of the individual
- [X] Has a type

**Every value in the RDF files:**

- [X] Is trimmed
- [X] Is properly encoded (e.g., dates, booleans)
- [X] Includes its datatype
- [X] Uses the correct datatype (e.g., values of 0-1 may be booleans and not integers, not every string made of numbers is a number)

## Comments on the self-assessment

We wrote one YARRRML file per dataset (`mappings/*.yml`) and translated each into RML (`mappings/*.rml`) with the YARRRML parser used by Matey. We then generated the RDF with Morph-KGC and saved it as Turtle (`rdf/*.ttl`). The mappings read the cleaned CSVs from Hands-on 3 and are run from the group folder, because the source paths start with `csv/`.

| Dataset | Mapping | RDF | Triples |
| --- | --- | --- | --- |
| Chicago Park District facilities | `mappings/CPD_Facilities.yml` / `.rml` | `rdf/CPD_Facilities.ttl` | 51,324 |
| Chicago Park District park art | `mappings/CPD_Park_Art.yml` / `.rml` | `rdf/CPD_Park_Art.ttl` | 5,465 |

Together the two files describe 555 parks, 4,466 facilities, 346 artworks, 264 artists, 20 owners and 4,812 coordinate nodes. The two datasets are linked through the park: both files build the same park URI from `PARK_NO`, so a park's facilities and artworks end up on one resource. `rdf/queries.sparql` holds the queries we used to verify the data, each with its expected result.

**Notes on the checklist**

- **Readable URIs:** parks use `ChicagoPark/{PARK_NO}`, and artists and owners use name slugs (`Artist/Phil_Schuster`, `Owner/Chicago_Park_District`). Facilities and artworks use the publisher's `OBJECTID` values (`Facility/1`, `Artwork/1`), as our resource naming strategy in `analysis.html` defines. These are stable identifiers from the Chicago Park District, not numbers we generated, but they are integers. For that reason we left this item unchecked.
- **Labels:** every individual has an `rdfs:label`. Parks, facilities, artworks, artists and owners use their name. The coordinate nodes have no name in the data, so their label is generated, e.g. `"Coordinates of facility 1"`.
- **Ontology terms:** we checked automatically that every class and property in the RDF is declared in `ontology/ontology.ttl`, and that each value matches the property's range: `xsd:integer` for park numbers and GIS IDs, `xsd:double` for coordinates, `xsd:string` for names, and IRIs of the right class for the object properties.
- **Missing values:** artworks with an unknown artist (31) or owner (54) get no `:madeBy` / `:owner` triple, so no placeholder resource is created. Two facilities and 38 artworks have no GIS ID, so they have no GIS ID triple.
- **Dates and booleans:** the datasets contain none.
