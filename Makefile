.ONESHELL:

.PHONY: help venv install run run_sync

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  install_all                      create local virtual environment, and install packages in local virtual environment"
	@echo "  install                          install packages in local virtual environment"
	@echo "  run                              run the sync script (without periodic sync)"
	@echo "  run_sync                         run the sync script (with periodic sync)"

venv:
	( \
	   python3 -m venv sync_venv; \
	   source sync_venv/bin/activate; \
	)

install: venv
	( \
	   source sync_venv/bin/activate; \
	   pip install -r requirements.txt; \
	)
	@echo "Virtual environment created, packages installed in sync_venv, use it with:\nsource sync_venv/bin/activate"

run:
	python3 src/sync.py

run_sync:
	python3 src/sync.py -sync