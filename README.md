# Apoy

[![Build Status](https://travis-ci.org/askeing/apoy.svg?branch=master)](https://travis-ci.org/askeing/apoy)

* Setup virtualenv
```bash
$ virtualenv env
$ source env/bin/activate
$ python setup.py develop
```
* Start [ngrok]
* Go to GitHub > Settings > OAuth applications > Developer Applications > Register new applications, input "<your ngrok url>/cb" to Authorization callback URL
* Save the `Client ID` and `Client Secret` to settings.json
* Run `python server.py` or `apoy`
* Open your ngrok url, e.g. `https://xxxxxxxx.ngrok.io` (You must use this url instead of `localhost:8888` otherwise cookies will not work)

[ngrok]: https://ngrok.com/download
