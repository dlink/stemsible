# stemsible

*Where Parents talk about their Kid's Education*

Stemsible is a Python 2.7 CGI Web App.

Production Site: http://crowfly.net/stemsible/main.py

Development Site: http://dev.crowfly.net/stemsible/main.py

## Installation:
```
apt-get install python-dev libmysqlclient-dev

pip install MySQL-python vlib vweb passlib jinja2 pillow

git clone git@github.com:dlink/stemsible.git
```

Set Environement Variables
```
cd ~/stemsible/bin
. ./aliases     # this creates the psdb, and dsdb aliases
. ./set_env.sh  # this sets PYTHONPATH, and VCONF
```

Install Database
```
# create a database on local host:

# create production database

cd ~/stemsible/sql
cat database_create.sql | mysql -uroot -p
cat build_all.sql | psdb --local-infile=1 -t

# create development database

cd ~/stemsible/sql
cat dev_database_create.sql | mysql -uroot -p
cat build_all.sql | dsdb --local-infile=1 -t
```

Configure
```
# review ~/stemsible/conf/dev.yml
# change your database settings if not on localhost
```

Test
```
cd ~/stemsible/tests
./test_all.sh
```

Apache Setup
```
cd /etc/apache2/sites-available
cp /home/USERNAME/stemsible/config/apache/stemsible.conf .
```

Create Session Data Folder
```
mkdir -p /data/stemsible/sessions
chgrp -R www-data /data/stemsible
chmod g+w /data/stemsible/sessions
```

Create Session Data Folder
```
mkdir -p /data/stemsible/sessions
```

Other python modules that will be needed
```
Cookie
json
sha
shelve
unittest
```
