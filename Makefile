.PHONY: lint check-keys release

# Packages each release container needs to run the key checker.
APT_KEYS_SETUP = apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq gpg ca-certificates python3 python3-yaml

lint:
	docker run --rm -v $(PWD):/workdir -w /workdir python:3-slim \
		sh -c "pip install -q -r requirements-dev.txt && ansible-galaxy install -r requirements.yml && ansible-lint"

# The live check runs in each release's own container, because whether a
# signature is accepted depends on that release's apt (trixie rejects SHA1
# bindings, bookworm does not). The script auto-detects the container's release.
RELEASES ?= bookworm trixie
check-keys:
	@for r in $(RELEASES); do echo "== $$r =="; \
		docker run --rm -v $(PWD):/workdir -w /workdir debian:$$r \
			sh -c "$(APT_KEYS_SETUP) && python3 scripts/check_apt_keys.py --live --days 30"; \
	done

release:
ifndef VERSION
	$(error VERSION is required, e.g. make release VERSION=v1.2.3)
endif
	./scripts/cut-release.sh $(VERSION)
