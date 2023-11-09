# Songs api using mongo + flask

Simple API for storing songs information, searching, sorting.


## To start project

```
docker-compose up
```

### To populate database

```
docker-compose exec songs_api python src/utils/populate_base.py
```

### To run tests

```
docker-compose exec songs_api pytest ./tests
```

### Run tests with coverage

```
docker-compose exec songs_api coverage run -m pytest ./tests
```

### Get coverage report
```
docker-compose exec songs_api coverage report -m
```
