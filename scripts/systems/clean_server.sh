. scripts/systems/envs.sh

incubator(){
    docker container kill incubator
    docker container rm incubator
}

db(){
    docker container kill mysql-test
    docker container rm mysql-test
}

emqx(){
    docker container kill emqx-test
    docker container rm emqx-test
}

if [[ $1 == "incubator" ]];
then
    incubator
elif [[ $1 == "db" ]];
then
    db
elif [[ $1 == "emqx" ]];
then
    emqx
elif [[ $1 == "all" ]];
then
    incubator
    db
    emqx
else
    echo "Unknown server to clean..."
fi
