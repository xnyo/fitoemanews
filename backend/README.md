## Fitoemanews backend
```
$ virtualenv -p $(which python3.6) .pyenv
$ source .pyenv/bin/activate
(.pyenv)$ pip install -r requirements.txt
(.pyenv)$ cp settings.sample.ini settings.ini
(.pyenv)$ nano settings.ini
...
(.pyenv)$ mysql -u fitoemanews -p fitoemanews < schema.sql
(.pyenv)$ python fitoemanews.py
```