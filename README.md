# Rysiek

Web based system which is a remedy for all pain concerns vcs monitoring in your continuous integration environment.
* Mirror git repositories
* Keep data up to date with origin
* Request for log using simple HTTP request
* Generate faboulus statistics
* Connect Rysiek with Jenkins and make them friends :)

### Development Status
---
Rysiek's core is written in Python with Django support. Application also uses Celery, CeleryBeat and Redis to execute background, scheduled tasks and make user experience more impressive! Currently Rysiek is under development, any version hasn't been released. If you have any idea and you would like to help building this awesome software, fell free to contact me: wojtek.biniek@gmail.com

### Developer's environment installation
---
##### Tool versions
* Python 3.6.4
* Django 2.0.3
* Django Rest Framework 3.7.7
* Celery 4.2.0
* Redis 2.10.6

##### Installation & Run of Django server
1. Set up virtualenv
```
$ python3.6 -m venv rysiek
$ source rysiek/bin/activate
```
2. Clone source code of Rysiek and install needed packages from requirements.txt
```
$ git clone https://github.com/biniow/rysiek rysiek_code
$ pip install -r rysiek_code/requirements.txt
```
3. Make migrations, create superuser and run Django server
```
$ cd rysiek_code/rysiek
$ ./manage.py migrate
$ ./manage.py createsuperuser
$ ./manage.py runserver
```
4. Great! Now you should be able to login to Django's admin page under URL: http://127.0.0.1:8000/admin/. You can login there using credentials provided during superuser creation process. You can add some repositories to be supported by Rysiek. Until CeleryBeat is not configured, it won't be mirrored, so you have to clone repo for tests under path provided in settings.py configuration file
```
$ cat rysiek/settings.py | grep REPO_STORAGE_PATH
REPO_STORAGE_PATH = '/tmp/repo_storage'
```
It can be changed by editing variable's value and restarting Django server.
##### Celery & Redis usage
Soon...

### API
---
Rysiek's power is great API which allows to browse mirrored repositories using simple HTTP requests
* `GET api/vcs/repositories` - lists all available repositories in system
* `GET api/vcs/repository/{id}` - retrieves details of single repository identified by `id` variable
* `GET api/vcs/repository/{id}/branches` - shows available branches in repository
* `GET api/vcs/repository/{id}/participants` - lists all participants by email with number of commits made
* `GET api/vcs/repository/{id}/log` - returns log of repository, which can be described by parameters:
    *   __start_rev__ - start revision from history
    *   __stop_rev__ - stop revision from history
    *   __branch__ - name of branch where history should be shown
    *   __author__ - filter by author
    *   __since__ - select only commits older than provided date
    *   __until__ - select only commits not older than provided date

##### Example of request:
```
$ curl -XGET http://127.0.0.1:8000/api/vcs/repository/1/log?since=10%20Mar%202018&until=17%20Jun%202018
{
    "repository_id": 1,
    "commits_returned": 3,
    "log": [
        {
            "hash": "1f98e8726aa1f90c7c18372875744a34fa2f15c8",
            "author": "wojtek <wojtek.biniek@gmail.com>",
            "date": "Sun Jun 17 22:13:06 2018 +0200",
            "commit_msg": "Changed approach to system. Cleaned models and API"
        },
        {
            "hash": "9139bee0af618df3b76ba088b3530781e023f6bf",
            "author": "wojtek <wojtek.biniek@gmail.com>",
            "date": "Sat Mar 10 01:02:40 2018 +0100",
            "commit_msg": "Celery configuration added"
        },
        {
            "hash": "591d1eeec43b53fc18cd72dbcfa63a9d3772795f",
            "author": "wojtek <wojtek.biniek@gmail.com>",
            "date": "Sat Mar 10 00:15:19 2018 +0100",
            "commit_msg": "Update of pip requirements"
        }
    ]
}
```
