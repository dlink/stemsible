# stemsible

*Where Parents talk about their Kid's Education*

Stemsible is a Python 2.7 CGI Web App.

Production Site: http://crowfly.net/stemsible/main.py

Development Site: http://dev.crowfly.net/stemsible/main.py

## Table Of Contents
<!-- MarkdownTOC -->

- [Installation](#installation)
    - [With Vagrant](#with-vagrant)
    - [Manual](#manual)
- [Development](#development)

<!-- /MarkdownTOC -->


## Installation

### With Vagrant

Clone the project:

```
git clone git@github.com:dlink/stemsible.git
cd stemsible
```

With [Vagrant](https://www.vagrantup.com/) and
[VirtualBox](https://www.virtualbox.org/) installed:
```
vagrant up
```

This may take up to 5-10 minutes depending on your machine and internet
connection. In the meantime add the line below to your hosts file:
```
192.168.33.22 local.stemsible.com
```

After your vm is provisioned go to the http://local.stemsible.com/


### Manual

*This installation has few steps missing here and there but will get you
a dev enviroment without a heavy VM*

```
apt-get install python-dev libmysqlclient-dev

pip install MySQL-python vlib vweb passlib jinja2 pillow itsdangerous sender

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

mysql -uroot -p
> create database stemsible;
> grant all on stemsible.* to stemsible@localhost identified by 'change-me';
> quit

cd ~/stemsible/sql
cat build_all.sql | psdb --local-infile=1 -t
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


## Development

SSH console to the vm
```
vagrant ssh
```

MySQL console
```
$ dsdb
```

App logs
```
$ tail -f log/stemsible.log
```

Run tests
```
$ cd stemsible/tests/
$ source test_all.sh
```
