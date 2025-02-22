# Variables
VENV_DIR=venv
PYTHON=$(VENV_DIR)/bin/python
PIP=$(VENV_DIR)/bin/pip

# Crear y activar el entorno virtual
venv:
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip --extra-index-url https://pypi.org/simple

# Instalar dependencias
install: venv
	$(PIP) install . --extra-index-url https://pypi.org/simple


# Ejecutar pruebas con pytest
test:
	pytest -v

# Formatear código con Black
format:
	black .

# Revisar errores con Flake8
lint:
	flake8 .

# Eliminar el entorno virtual
clean:
	rm -rf $(VENV_DIR) __pycache__

# Regenerar el entorno virtual y reinstalar dependencias
reset: clean venv install

# Ejecutar migraciones con Alembic (si usas migraciones)
migrate:
	alembic upgrade head

# Crear un nuevo archivo de migración (si usas Alembic)
makemigrations:
	alembic revision --autogenerate -m "Nueva migración"
