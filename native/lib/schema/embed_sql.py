#!/usr/bin/env python3
"""Generate native/lib/schema embedded_schemas.hpp from data/schema/*.sql."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 4:
        print("Usage: embed_sql.py <world_v1.sql> <playthrough_v1.sql> <out.hpp>", file=sys.stderr)
        return 1

    world_sql = Path(sys.argv[1]).read_text(encoding="utf-8")
    playthrough_sql = Path(sys.argv[2]).read_text(encoding="utf-8")
    out_path = Path(sys.argv[3])
    out_path.parent.mkdir(parents=True, exist_ok=True)

    content = (
        "#pragma once\n\n"
        "namespace neon::schema {\n\n"
        f'inline constexpr const char* kWorldV1Sql = R"NEON_SQL({world_sql})NEON_SQL";\n\n'
        f'inline constexpr const char* kPlaythroughV1Sql = R"NEON_SQL({playthrough_sql})NEON_SQL";\n\n'
        "} // namespace neon::schema\n"
    )
    if not out_path.exists() or out_path.read_text(encoding="utf-8") != content:
        out_path.write_text(content, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
