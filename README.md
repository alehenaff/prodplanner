prodplanner
===========


Django DRF project to calculate dates for reccuring actions

Based on dateutil ; it is possible to define rrules and dates and create rrulesets including or excluding rrulesets, rrules or dates.

To perform it :

* rrules are defined at '/planner/simplerules/',
* dates at '/planner/daterules/'
* rrulesets at '/planner/rulesets/'
* including or excluding elements from a rruleset at '/planner/rulesetelements/'

it is then possible to query a rruleset to get occurences on a time interval :

http://localhost:8000/planner/rulesets/4/between/?start=2017-01-01T00:00:00&end=2019-01-01T00:00:00

```
HTTP 200 OK
Allow: GET, OPTIONS
Content-Type: application/json
Vary: Accept

[
    "2017-04-17T00:00:00",
    "2017-07-14T00:00:00",
    "2017-12-25T00:00:00",
    "2018-04-02T00:00:00",
    "2018-07-14T00:00:00",
    "2018-12-25T00:00:00"
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
