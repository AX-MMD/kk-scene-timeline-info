.DEFAULT_GOAL := all
src_path = src
project_path = $(src_path)/kk_scene_timeline_info
mypylint = mypy $(project_path) --ignore-missing-imports --no-warn-unused-ignores --warn-redundant-casts --warn-unused-ignores --pretty --show-error-codes --check-untyped-defs

.PHONY: pretty
pretty:
    ruff format $(project_path)

.PHONY: format
format:
    ruff format $(project_path)
    ruff check --fix
    $(mypylint)

.PHONY: lint
lint:
    ruff check
    $(mypylint)

.PHONY: test
test:
    pytest $(project_path)

.PHONY: run
run:
    python $(src_path)/main.py

.PHONY: bin
bin:
    cxfreeze build

.PHONY: release
release:
    $(MAKE) lint
    $(MAKE) test
    $(MAKE) bin
    python $(src_path)/make_release.py

.PHONY: all
all: lint test