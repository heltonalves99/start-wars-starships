# Star Wars

Starships from the Star Wars movies

[![Build Status](https://travis-ci.org/heltonalves99/start-wars-starships.svg?branch=master)](https://travis-ci.org/heltonalves99/start-wars-starships)


## Installing dependencies

Requires Python 3.7 or later.
To install dependencies in a virtual environment using Pipenv:
More information available in the [Pipenv documentation](https://pipenv.readthedocs.io/en/latest/).

```
$ pipenv install
```

To activate the virtual environment:

```
$ pipenv shell
```

## Starting the application

### Development

To run the application in development mode:

```
$ FLASK_APP=api FLASK_ENV=development flask run
 * Serving Flask app "api" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 283-128-423
```

## Testing

Unit tests are written using the PyTest framework.

To run unit tests:

```
$ pipenv run python -m pytest
==================================== test session starts ====================================
platform darwin -- Python 3.7.2, pytest-5.0.1, py-1.8.0, pluggy-0.12.0
rootdir: /Users/heltonalves/Projects/start-wars-starships
collected 1 item

tests/test_starships.py .                                          [100%]

==================================== 1 passed in 2.64 seconds ====================================
```
