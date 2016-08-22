# stemsible

*Where Parents talk about their Kid's Education*

Stemsible is a Python 2.7 CGI Web App.

Production Site: http://crowfly.net/stemsible/main.py

Development Site: http://dev.crowfly.net/stemsible/main.py

## Installation (using Vagrant):

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
