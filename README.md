# common-for-services

```
common/
│── __init__.py
│── middleware/
│   │── __init__.py
│   │── db_transaction.py
│   │── logging.py
│   │── authentication.py
│── database/
│   │── __init__.py
│   │── connection.py
│── utils/
│   │── __init__.py
│   │── alerts.py
│   │── monitoring.py
│── setup.py  # If packaging as an installable module
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

