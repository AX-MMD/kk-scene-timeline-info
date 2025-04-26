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
    pyinstaller run_gui.spec
	rm -rf ./dist
	mkdir -p ./dist
    mv -f ./dist/KoikatsuPlapGenerator.exe $(src_path)/bin/KoikatsuPlapGenerator.exe
    rsync -a --remove-source-files ./dist/__internal__/ $(src_path)/bin/__internal__/
    rm -rf ./dist/__internal__

.PHONY: release
release: lint test bin
    python $(src_path)/make_release.py

.PHONY: all

all: lint test
