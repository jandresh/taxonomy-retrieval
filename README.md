# taxonomy-retrieval

A two-step pipeline to retrieve NCBI taxonomic lineage for a list of species and visualize their taxonomic distribution.

## Overview

Given a plain-text list of species names, this pipeline:

1. Converts each species name to its NCBI Taxonomy ID (TaxID).
2. Retrieves the full taxonomic lineage for each TaxID and generates an interactive sunburst visualization.

## Requirements

- [ete3](http://etetoolkit.org/) (`pip install ete3`)
- [Plotly](https://plotly.com/python/) (`pip install plotly`)
- The NCBI taxonomy dump (`taxdump.tar.gz`) — included in each step directory or downloadable from [NCBI](https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz)

## Pipeline

### Step 1 — Convert species names to TaxIDs

**Directory:** `1_convert_to_taxid/`

**Input:** `species.txt` — one species name per line (e.g. `Homo sapiens`).

**Script:** `readline.sh`

```bash
bash readline.sh > taxids_output.txt
```

This calls `ete3 ncbiquery --info` for each species and extracts the TaxID. The raw output may contain `SyntaxWarning` lines from ete3 internals; filter them to produce a clean file:

```bash
grep -E '^[0-9]+$' taxids_output.txt > taxids_output.fixed.txt
```

**Output:** `taxids_output.fixed.txt` — one numeric TaxID per line.

---

### Step 2 — Retrieve lineage and visualize

**Directory:** `2_recover_lineage/`

**Input:** `taxids_output.fixed.txt` (copied from step 1).

**Script:** `get_ncbi_taxonomy.py`

```bash
python get_ncbi_taxonomy.py
```

For each TaxID the script queries the local NCBI taxonomy database and resolves the full lineage across eight ranks:

`superkingdom → kingdom → phylum → class → order → family → genus → species`

**Outputs:**

| File | Description |
| --- | --- |
| `full_ranks.txt` | Tab-separated file with the resolved lineage IDs for every species |
| `outputSunburst.html` | Interactive sunburst chart of the taxonomic tree |
| `outputTreemap.html` | Interactive treemap of the taxonomic tree |

The visualization colors each species according to its community assignment (from `SpeciesListTaxAPOE.txt` and the community matrix embedded in the script).

## Repository structure

```text
taxonomy-retrieval/
├── 1_convert_to_taxid/
│   ├── species.txt                  # Input: species names
│   ├── readline.sh                  # Converts names → TaxIDs
│   ├── taxids_output.txt            # Raw output (may contain warnings)
│   ├── taxids_output.fixed.txt      # Cleaned TaxIDs, one per line
│   └── expected_output_files/       # Reference outputs for validation
├── 2_recover_lineage/
│   ├── taxids_output.fixed.txt      # Input: TaxIDs from step 1
│   ├── SpeciesListTaxAPOE.txt       # Species list with community data
│   ├── get_ncbi_taxonomy.py         # Retrieves lineage and builds charts
│   ├── full_ranks.txt               # Output: resolved lineage table
│   ├── outputSunburst.html          # Output: sunburst visualization
│   ├── outputTreemap.html           # Output: treemap visualization
│   └── expected_output_files/       # Reference outputs for validation
└── LICENSE
```

## License

MIT — see [LICENSE](LICENSE).
