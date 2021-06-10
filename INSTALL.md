# Shorten URL service

## Installation instructions

1. Clone the repo. Additional instructions (credentials) can be found [here](https://app.codesubmit.io/c/finn-gmbh/08f53aee-efa6-4ba5-8c74-b9260287d048/90496266-d2d5-4359-b357-c630c9c9240c).

```bash
$ git clone https://finn-gmbh-dreamy-banach@git.codesubmit.io/finn-gmbh/the-shortest-url-1-wcbrhr
$ cd the-shortest-url-1-wcbrhr
```


2. Setup a python virtual environment and install dependencies.

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install --upgrade pip wheel setuptools
$ pip install -r requirements.txt
$ python setup.py develop
```

3. Create the `instance/config.json` file. A sample with smart defaults is provided which can be copied from.

```bash
cp config.json.sample instance/config.json
```


## Export environment variables

```bash
$ export FLASK_APP=shorturl
$ export FLASK_ENV=development
```

## Initialize the database

```bash
$ flask init-db
```

## Run the server locally

```bash
$ flask run
```

## Launch SwaggerUI

Navigate to http://localhost:5000/apidocs.

## Build and view API docs

```bash
$ cd docs
$ sphinx-apidoc --force -o . ..
$ make html
```
> See Known Issues below.

Use a web browser to open `_build/html/index.html`

## Run tests
```bash
$ pytest
```
> See Known Issues below.
## Via cURL

While SwaggerUI is perfectly capable when it comes to evaluating the service, cURL commands can also be used.

### sample `/encode`
```bash
$ curl --location --request POST 'localhost:5000/encode' \
--header 'Content-Type: application/json' \
--data-raw '{"url": "https://codesubmit.io/library/react"}'
```

### sample `/decode`
```bash
$ curl --location --request POST 'localhost:5000/decode' \
--header 'Content-Type: application/json' \
--data-raw '{
  "short_url": "https://short.est/867nv"
}'
```

## Known issues
- An `sqlite3.ProgrammingError` exception is thrown while exiting the server. 
```
sqlite3.ProgrammingError: SQLite objects created in a thread can only be used in that same thread.
```
- Running tests via `pytest` raises a `DeprecationWarning` for the `imp` module used by `flassger`.
- Generating docs raises an `Unexpected indentation` warning. This is due to the Swagger documentation for the endpoints.

## Other notes
- Although an in-memory storage was sufficient according to the requirements, citing thread-safety concerns, a simple SQLite (file based) database was used instead.
- By design, the same URL returns a new short URL each time.This opens up the possibility of each individually tracking each short URL (e.g. to keep track of users).

## TODO
- As of now, `loguru` is being used to log to STDOUT only. A file handler needs to be added while initializing `loguru` so that logs are persisted to files as well.
- The API response structure is crude at best for now. Need to implement a class so that it is more extensible.

## Troubleshooting
If you see an error similar to this:
```
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: urls_map
[SQL: SELECT urls_map.id AS urls_map_id, urls_map.short_url AS urls_map_short_url, urls_map.original_url AS
urls_map_original_url, urls_map.created_at AS urls_map_created_at
FROM urls_map
WHERE urls_map.id = ?]
[parameters: (1,)]
(Background on this error at: http://sqlalche.me/e/14/e3q8) // Werkzeug Debugger
```
You probably missed running `flask init-db`.