. scripts/tools/envs.sh

if [[ $1 == "event" ]];
then
    python -m app.create_event_db
elif [[ $1 == "api" ]];
then
    if [[ -z $2 ]];
    then
        echo "missing target container!!!"
        exit 0
    fi

    echo "running command in container: $2"
    docker exec $2 bash scripts/rebuild_database.sh

else
    echo "Unknown server to db to initialize..."
fi
