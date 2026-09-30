#!/usr/bin/env bash
# doctor — retrato do estado do ambiente DBurger em camadas.
# Exit: 0 = pronto, 1 = erro, 3 = dependência ausente.
set -u

fail=0
missing=0

layer() { printf '%-14s %s\n' "$1" "$2"; }

if command -v docker >/dev/null 2>&1; then
  layer "docker" "ok ($(command -v docker))"
else
  layer "docker" "AUSENTE — instale o Docker (ou colima/orbstack)"
  missing=1
fi

if docker info >/dev/null 2>&1; then
  layer "daemon" "ok"
else
  layer "daemon" "PARADO — rode 'colima start' (ou inicie seu runtime Docker)"
  missing=1
fi

if docker image inspect "${DBURGER_ORACLE_IMAGE:-gvenzl/oracle-free:slim}" >/dev/null 2>&1; then
  layer "imagem" "ok (${DBURGER_ORACLE_IMAGE:-gvenzl/oracle-free:slim})"
else
  layer "imagem" "ausente — 'make test-integration' baixa automaticamente"
fi

container="${DBURGER_ORACLE_CONTAINER:-dburger-oracle}"
status="$(docker inspect -f '{{.State.Status}}' "$container" 2>/dev/null || echo ausente)"
layer "contêiner" "$status ($container)"

if [ "$status" = "running" ]; then
  if docker exec "$container" /home/oracle/healthcheck.sh >/dev/null 2>&1; then
    layer "oracle" "pronto"
  else
    layer "oracle" "subindo — aguarde (~1–2 min)"
  fi
  if docker exec -i -e NLS_LANG=AMERICAN_AMERICA.AL32UTF8 "$container" \
       sqlplus -s "system/${DBURGER_SYS_PASSWORD:-dburger_dev_only}@//localhost:1521/FREEPDB1" \
       <<'SQL' >/dev/null 2>&1
SELECT 1 FROM dual;
EXIT
SQL
  then
    layer "sqlplus" "ok (contêiner)"
  else
    layer "sqlplus" "falhou — confira DBURGER_SYS_PASSWORD vs ORACLE_PASSWORD do contêiner"
    fail=1
  fi
fi

echo
if [ "$missing" -eq 1 ]; then
  echo "dependência ausente (exit 3) — corrija a camada indicada acima"
  exit 3
fi
if [ "$fail" -eq 1 ]; then
  echo "erro (exit 1) — veja a camada com falha"
  exit 1
fi
echo "pronto (exit 0)"
