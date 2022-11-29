. scripts/systems/envs.sh

incubator(){
    docker commit incubator incubator:$2
    docker container kill incubator
    docker container rm incubator
    bash scripts/systems/start_server.sh $1 $2

}

db(){

    docker commit mysql-test mysql-test:$2
    docker container kill mysql-test
    docker container rm  mysql-test
    bash scripts/systems/start_server.sh $1 $2
}

if [[ -z $2 ]];
then
    echo "Commit name not specified..."
    exit -1
fi

if [[ $1 == "incubator" ]];
then
    incubator $1 $2
elif [[ $1 == "db" ]];
then
    db $1 $2
else
    echo "Unknown server to commit..."
fi