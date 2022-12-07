. scripts/systems/envs.sh

incubator(){
   
    if [[ -z $1 ]];
    then
        IMAGE="incubator:init"
    else
        IMAGE="incubator:$1"
    fi



   docker run -dt \
        -v $BACKEND_SERVER_DOCKER_CONTEXT:/app/ \
        --env-file "$BACKEND_SERVER_DOCKER_CONTEXT/.env" \
        -p 80:80 \
        --network $DOCKER_NETWORK \
        --name incubator \
        incubator:init \
        bash -c "mkdir -p /app/logs && python -m app.server_uvicorn"

}

db(){
    
    docker run -dt \
        -p 27001:3306 \
        -e MYSQL_DATABASE=foxlink \
        -e MYSQL_ROOT_PASSWORD=AqqhQ993VNto \
	-v /root/foxlink-testing/mysql-db:/var/lib/mysql\
        --name mysql-test \
        --network $DOCKER_NETWORK \
        mysql:8

}

emqx(){
    docker run -dt \
        -p 1883:18083 \
        -p 18083:1883 \
        --name emqx-test \
        --network $DOCKER_NETWORK\
        emqx/emqx
}

if [[ $1 == "incubator" ]];
then
    incubator $2
elif [[ $1 == "db" ]];
then
    db $2
elif [[ $1 == "emqx" ]];
then
    emqx $2
elif [[ $1 == "all" ]];
then
    db $2
    sleep 5
    emqx $2
    sleep 5
    incubator $2
else
    echo "Unknown server to start..."
fi
