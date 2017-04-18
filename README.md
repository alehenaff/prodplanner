prodplanner
===========


Django DRF project to calculate dates for reccuring actions

Based on dateutil ; it is possible to define rrules and dates and create rrulesets including or excluding rrulesets, rrules or datetimes.

The first goal is to get a list of dates, not datetimes.

To perform it :

* rrules are defined at '/planner/simplerules/',
* dates at '/planner/daterules/'
* rrulesets at '/planner/rulesets/'
* including or excluding elements from a rruleset at '/planner/rulesetelements/'

it is then possible to query a rruleset to get occurences on a time interval :

http://localhost:8000/planner/rulesets/a66d4242-8e2e-43bd-ba49-3970dc51ca28/between/?start=2017-01-01T00:00:00&end=2018-01-01T00:00:00

```
HTTP 200 OK
Allow: GET, OPTIONS
Content-Type: application/json
Vary: Accept

[

    "2017-01-01",
    "2017-04-17",
    "2017-05-01",
    "2017-05-08",
    "2017-05-26",
    "2017-06-05",
    "2017-07-14",
    "2017-08-15",
    "2017-11-01",
    "2017-11-11",
    "2017-12-25",
    "2018-01-01"
]
```
It is also possible to get next 10 occurences for a ruleset :

http://localhost:8000/planner/rulesets/a66d4242-8e2e-43bd-ba49-3970dc51ca28/next10/
```
[
    "2017-05-01",
    "2017-05-08",
    "2017-05-26",
    "2017-06-05",
    "2017-07-14",
    "2017-08-15",
    "2017-11-01",
    "2017-11-11",
    "2017-12-25",
    "2018-01-01"
]
```

python manage.py makemigrations

python manage.py migrate

Load fixtures : python manage.py loaddata fixtures/planner.json



# version
Alpha developpement

# tested with

* Python 3.5.3
* Django 1.10.6

# todo
* make it as a library or django-app
* ... suggestions welcomed
