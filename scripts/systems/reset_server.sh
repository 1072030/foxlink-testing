. scripts/systems/envs.sh

commit(){
    if [[ -z $CONTAINER ]];
    then
        echo "unknown container to proceed"
        exit -1
    fi

    if [[ ! -z $1 ]];
    then
        docker commit $CONTAINER $CONTAINER:$1
        TAG=$1
    else
        TAG=init
    fi
}

restart(){
    docker container kill $CONTAINER
    docker container rm  $CONTAINER
    bash scripts/systems/start_server.sh $SERVER $TAG
}

incubator(){
    CONTAINER=incubator
    SERVER=incubator
    commit $1
    restart
}

db(){
    CONTAINER=mysql-test
    SERVER=db
    commit $1
    restart
}

emqx(){
    CONTAINER=emqx-test
    SERVER=emqx
    commit $1
    restart
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