# common-for-services

```
common_for_services/                          # Carpeta Raíz
├── 📂 src/                                   # Carpeta que contiene el código fuente
│    ├── 📂 database/                         # Configuración de la base de datos
│    │   ├── __init__.py                      # Inicialización del módulo de base de datos
│    │   ├── connection.py                    # Conexión a la base de datos
│    ├── 📂 middleware/                       # Middleware para la lógica de procesamiento
│    │   ├── __init__.py                      # Inicialización del módulo de middleware
│    │   ├── db_transaction.py                # Manejo de transacciones de base de datos
│    │   ├── logging.py                       # Lógica de manejo de logs
│    ├── 📂 notification/                     # Módulo para notificaciones
│    │   ├── __init__.py                      # Inicialización del módulo de notificaciones
│    │   ├── alerts.py                        # Lógica de alertas
│    │   ├── slack.py                         # Integración con Slack para notificaciones
│    │   ├── sms_twilio.py                    # Integración con Twilio para SMS
│    │   ├── smtp.py                          # Integración con SMTP para correos electrónicos
│    │   ├── web_hook.py                      # Integración con Webhooks para notificaciones
│    ├── 📂 tasks/                            # Tareas en segundo plano (por ejemplo, con Celery)
│    │   ├── celery_worker.py                 # Configuración del worker de Celery para tareas en segundo plano
│    ├── __init__.py                          # Inicialización del módulo principal
├── 📄 .gitignore                             # Archivos y directorios ignorados por Git
├── 📄 Makefile                               # Archivo de automatización para tareas comunes
├── 📄 pyproject.toml                        # Configuración del proyecto y dependencias
├── 📄 README.md                              # Descripción general del proyecto

```

### Build the package
```
python setup.py sdist bdist_wheel
```

### Install pakage
```
pip install git+https://github.com/personal-projects-luismh92/common-for-services.git@develop --extra-index-url https://pypi.org/simple
```

```
pip install git+https://github.com/personal-projects-luismh92/common-for-services.git
```

