# yousician

#To start project

docker-compose up

#To populate database

docker-compose exec songs_api python src/utils/populate_base.py

#To run tests

docker-compose exec songs_api pytest ./tests