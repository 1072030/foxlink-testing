. scripts/systems/envs.sh

incubator(){
   
    if [[ -z $1 ]];
    then
        IMAGE="incubator:init"
    else
        IMAGE="incubator:$1"
    fi

    docker run -dt \
        -v $BACKEND_SERVER_DOCKER_CONTEXT:/code/ \
        --env-file "$BACKEND_SERVER_DOCKER_CONTEXT/.env" \
        -p 9090:8080 \
        --network $DOCKER_NETWORK \
        --name incubator \
        $IMAGE \
        bash

}

db(){

    if [[ -z $1 ]];
    then
        IMAGE="mysql-test:init"
    else
        IMAGE="mysql-test:$1"
    fi
    
    docker run -dt \
        -p 27001:3306 \
        -e MYSQL_DATABASE=foxlink \
        -e MYSQL_ROOT_PASSWORD=AqqhQ993VNto \
        --name mysql-test \
        --network $DOCKER_NETWORK \
        $IMAGE

}

emqx(){
    docker run -dt \
        -p 18083:18083 \
        -p 1883:1883 \
        -p 8083:8083 \
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
    incubator $2
    db $2
    emqx $2
else
    echo "Unknown server to start..."
fi