# context_switcher.py
"""
Temple Codex / Weave OS
Dynamic Context Switcher v1.0
Loads theological or cultural symbol overrides dynamically.
"""

import json
from pathlib import Path

def load_symbols(base_path="weave_symbols.json", overrides_path="symbol_overrides.json", context=None):
    base = json.loads(Path(base_path).read_text(encoding="utf-8"))
    overrides = json.loads(Path(overrides_path).read_text(encoding="utf-8"))

    if not context:
        return base  # no override, return defaults

    merged = base.copy()
    ctx_map = overrides.get("contexts", {}).get(context, {})

    # Apply overrides shallowly (vows + axioms + substructures)
    for group in ["vows", "axioms", "movements", "substructures"]:
        if group in merged:
            for key, entry in merged[group].items():
                symbol_override = ctx_map.get(key)
                if symbol_override:
                    entry["symbol"] = symbol_override

    # Allow direct symbol replacements (e.g., meta glyphs)
    if "meta_symbols" in merged:
        for k, v in merged["meta_symbols"].items():
            if k in ctx_map:
                merged["meta_symbols"][k] = ctx_map[k]

    print(f"Loaded context: {context}")
    return merged


if __name__ == "__main__":
    # Example usage
    symbols = load_symbols(context="buddhist")
    for key, data in symbols["vows"].items():
        print(f"{key.title()}: {data['symbol']} — {data['essence']}")
