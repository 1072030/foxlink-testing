ssh ntust-foxlink@140.118.157.9 -p 7869 \
"docker network $1 foxlink-api-backend_backend foxlink-api-backend_foxlink-backend_1; \
docker network $1 foxlink-api-backend_backend foxlink-api-backend_foxlink-daemon_1; \
docker network $1 foxlink-api-backend_backend foxlink-api-backend_mysql_1;"


if [[ $1 == "event" ]];
then
    python -m app.create_event_db
elif [[ $1 == "api" ]];
then
    # 
else
    echo "Unknown server to db to initialize..."
fi