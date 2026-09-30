.PHONY: test vet lint build doctor test-integration clean

# Contrato estrutural — offline, sem Oracle (não prova comportamento).
test:
	python3 tests/test_offline.py

# Contrato de declaração + golden file (subconjunto rápido).
vet:
	python3 tests/test_offline.py --vet

# Comportamento — execução real em Oracle (marcador: integration).
test-integration:
	python3 tests/run_tests.py

lint:
	bash scripts/lint.sh

build:
	mkdir -p dist
	cat src/rn01_bloco.sql > dist/dburger-rn01.sql
	@echo "build: dist/dburger-rn01.sql"

doctor:
	bash scripts/doctor.sh

clean:
	rm -rf dist
