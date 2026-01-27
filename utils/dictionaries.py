import csv
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_contributor_systems():
    """
    Returns:
      dict[str, float]
      { "QUEST_NI": 18733999.00, ... }
    """
    path = DATA_DIR / "contributor_systems.tsv"
    mapping = {}

    if not path.exists():
        return mapping

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            if len(row) != 2:
                continue
            code, name = row
            mapping[name.strip()] = float(code)

    return mapping


def load_error_dictionary():
    """
    Returns:
      list[dict]
      [
        {
          "severity": "FAILURE",
          "error_pattern": "...",
          "summary": "...",
          "recommended_action": "...",
          "ccl_tags": ["order", "alias"]
        }
      ]
    """
    path = DATA_DIR / "error_dictionary.tsv"
    entries = []

    if not path.exists():
        return entries

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            row["ccl_tags"] = [
                t.strip() for t in row.get("ccl_tags", "").split(",") if t.strip()
            ]
            entries.append(row)

    return entries
