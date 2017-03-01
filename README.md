# Openedoo module_employee

Module for managing employee inspired from JIBAS.

## Instalation

Install this module inside Openedoo
```
$ openedoo manage.py module install https://github.com/openedoo/module_employee
```
Then update your database
```
$ openedoo manage.py db upgrade
$ openedoo manage.py db migrate
```

## UI Developing
Use Gulp for compiling sass files inside `module_employee`
```
$ npm install
$ gulp
```

## #TODO: list
* Update existing employee data
* Make codebase more modular and clean
* Better notification message
* Validate unique data
