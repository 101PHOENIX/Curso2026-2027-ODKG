import os
from pathlib import Path

import morph_kgc


def main():
    group_dir = Path(__file__).resolve().parent.parent
    rdf_dir = group_dir / "rdf"

    # Paths in config.ini are relative to Group07.
    os.chdir(group_dir)

    graph = morph_kgc.materialize("transformation/config.ini")

    rdf_dir.mkdir(exist_ok=True)

    graph.serialize(
        destination=str(rdf_dir / "knowledge-graph.ttl"),
        format="turtle",
    )

    print(f"Generated {len(graph)} triples")


if __name__ == "__main__":
    main()
