## Fitoemanews backend
```
$ virtualenv -p $(which python3.6) .pyenv
$ source .pyenv/bin/activate
(.pyenv)$ pip install -r requirements.txt
(.pyenv)$ cp settings.sample.ini settings.ini
(.pyenv)$ nano settings.ini
...
(.pyenv)$ python fitoemanews.py migrate
...
(.pyenv)$ python fitoemanews.py
```