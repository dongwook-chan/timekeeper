## Getting Started
```bash
# git clone
$ git clone {repo URL}
$ cd {repo name}
# create & activate venv
$ python3 -m venv env
$ source env/bin/activate
(env) $ python3 -m pip install -r requirements.txt
# activate pre-commit hooks
(env) $ pre-commit install
```
## TODO
* Listen to & handle task edit event
* Can listen to Clikcup triggered event?
* duplicate events created
* log 
* color scheme (productivity vs non-, evaluation)
* restart script
* include venv activation in start/restart script
* clickup automation
* start server on boot
* timesheet: bulk get events and update to calendar if not duplicate
