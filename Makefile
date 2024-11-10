SHELL := /bin/bash
CWD := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
ME := $(shell whoami)

nothing:
	@echo "do nothing"

clean_up:
	docker system prune -a
	docker volume prune -a

fix_permissions:
	@echo "me: $(ME)"
	sudo chown $(ME):$(ME) -R .

lint:
	poetry run ruff ./src
	poetry run black --check
	poetry run isort --check

format:
	poetry run black
	poetry run isort

build:
	docker compose build

drop:
	docker compose down -v

up:
	docker compose up --remove-orphans --build \
		chat_bot \
		ollama_serve \
		mongodb \
		mongodb-express