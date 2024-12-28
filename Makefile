#VENV = ./venv/bin/activate
#vars
VENV = ./.venv/bin/activate
RUNFILE = bot.py
SHELL = /bin/bash
EXEC = ./.venv/bin/python

.PHONY: all install venv

.ONESHELL:
all: venv install
	git pull
	$(EXEC) $(RUNFILE)

install:
	$(EXEC) -m pip install -r requirements.txt

venv:
	python -m venv .venv
	. $(VENV)