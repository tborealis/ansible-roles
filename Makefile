.PHONY: lint release

lint:
	docker run --rm -v $(PWD):/workdir -w /workdir python:3-slim \
		sh -c "pip install -q -r requirements-dev.txt && ansible-galaxy install -r requirements.yml && ansible-lint"

release:
ifndef VERSION
	$(error VERSION is required, e.g. make release VERSION=v1.2.3)
endif
	./scripts/cut-release.sh $(VERSION)
