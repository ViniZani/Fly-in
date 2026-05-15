SHELL    := /bin/sh
VENV_DIR := .venv
PYTHON   := $(VENV_DIR)/bin/python
PIP      := $(VENV_DIR)/bin/pip
FLAKE8   := $(VENV_DIR)/bin/flake8
MYPY     := $(VENV_DIR)/bin/mypy
FILE ?= simple_fork.txt


all: run



help:
	@echo "Install: make install"
	@echo "Use: make run FILE=you_map.txt"

install:
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install flake8 mypy build
	$(PIP) install -e .


run:
	$(PYTHON) main.py $(FILE)


debug:
	$(PYTHON) -m pdb main.py $(FILE)


clean:
	rm -rf .mypy_cache .pytest_cache .build build dist *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete


fclean: clean
	rm -rf $(VENV_DIR)


lint:
	$(FLAKE8) . --exclude=$(VENV_DIR)
	$(MYPY) . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs


lint-strict:
	$(FLAKE8) . --exclude=$(VENV_DIR)
	$(MYPY) . --strict


re: fclean install

.PHONY: all install run debug clean fclean lint lint-strict re