.PHONY: lint

lint:
	docker run --rm -v $(PWD):/workdir -w /workdir python:3-slim \
		sh -c "pip install -q -r requirements-dev.txt && ansible-galaxy install -r requirements.yml && ansible-lint"
