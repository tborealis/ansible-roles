.PHONY: lint check-keys release

lint:
	docker run --rm -v $(PWD):/workdir -w /workdir python:3-slim \
		sh -c "pip install -q -r requirements-dev.txt && ansible-galaxy install -r requirements.yml && ansible-lint"

check-keys:
	docker run --rm -e DEBIAN_FRONTEND=noninteractive -v $(PWD):/workdir -w /workdir debian:trixie \
		sh -c "apt-get update -qq && apt-get install -y -qq gpg ca-certificates python3 python3-yaml && python3 scripts/check_apt_keys.py --live --days 30"

release:
ifndef VERSION
	$(error VERSION is required, e.g. make release VERSION=v1.2.3)
endif
	./scripts/cut-release.sh $(VERSION)
