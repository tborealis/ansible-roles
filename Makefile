.PHONY: lint

lint:
	docker run --rm -v $(PWD):/workdir cytopia/ansible-lint:latest /workdir
