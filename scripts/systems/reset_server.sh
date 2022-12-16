. scripts/systems/envs.sh

commit(){
    if [[ -z $CONTAINER ]];
    then
        echo "unknown container to proceed"
        exit -1
    fi

    if [[ $1 == "comit" ]];
    then
        if [[ ! -z $2 ]];
        then
            docker commit $CONTAINER $CONTAINER:$2
            TAG=$2
        else
            echo "commit requires a tag..."
            exit -1
        fi
    elif [[ ! -z $1 ]];
    then
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
    commit $1 $2
    restart
}

db(){
    CONTAINER=mysql-test
    SERVER=db
    commit $1 $2
    restart
}

emqx(){
    CONTAINER=emqx-test
    SERVER=emqx
    commit $1 $2
    restart
}

if [[ $1 == "incubator" ]];
then
    incubator $2 $3
elif [[ $1 == "db" ]];
then
    db $2 $3
elif [[ $1 == "emqx" ]];
then
    emqx $2 $3
elif [[ $1 == "init" ]];
then
    incubator
    db
    emqx
else
    echo "Unknown server to start..."
fi