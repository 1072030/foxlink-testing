python app/utils/delete.py
docker-compose kill autoworker
docker-compose kill autocreate
docker-compose up --build -d autocreate
docker-compose up --build autoworker