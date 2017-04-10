# Openedoo module_employee

Module for managing employee inspired from JIBAS.

## Instalation

Install this module inside Openedoo
```
$ python manage.py module install https://github.com/openedoo/module_employee
```

Update file in `openedoo_project/tables.py`
```
from modules.module_employee import models
```

Then update your database
```
$ python manage.py db upgrade
$ python manage.py db migrate
```

You can see this modules at
```
http://<your-host>/employee
```


## UI Developing
Use Gulp for compiling sass files inside `module_employee`
```
$ npm install
$ gulp
```

## #TODO: list
* Make codebase more modular and clean
* Better notification message
* Validate unique data
