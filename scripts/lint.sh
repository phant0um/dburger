#!/usr/bin/env bash
# lint — gitleaks (segredos) + higiene de texto (EOL final, sem trailing space).
set -u
cd "$(dirname "$0")/.."

if command -v gitleaks >/dev/null 2>&1; then
  if gitleaks dir --help >/dev/null 2>&1; then
    gitleaks dir --no-banner --redact . || exit 1
  else
    gitleaks detect --no-banner --redact . || exit 1
  fi
else
  echo "lint: gitleaks ausente (exit 3)" >&2
  exit 3
fi

python3 - <<'PY'
import pathlib, sys

bad = []
for p in pathlib.Path(".").rglob("*"):
    if not p.is_file() or ".git" in p.parts or "dist" in p.parts:
        continue
    try:
        data = p.read_bytes()
    except OSError:
        continue
    if b"\0" in data:
        continue
    text = data.decode("utf-8", errors="replace")
    for i, line in enumerate(text.splitlines(), 1):
        if line != line.rstrip():
            bad.append(f"{p}:{i}: trailing whitespace")
    if text and not text.endswith("\n"):
        bad.append(f"{p}: sem newline final")
if bad:
    print("lint de texto REPROVADO:")
    print("\n".join(bad[:20]))
    sys.exit(1)
print("lint: gitleaks ok, texto ok")
PY
