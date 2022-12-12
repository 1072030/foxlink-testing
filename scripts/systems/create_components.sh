. scripts/systems/envs.sh
# create backend server image
cd $BACKEND_SERVER_DOCKER_CONTEXT
docker build -t incubator:init . -f $BACKEND_SERVER_DOCKER_FILE
# create testing database image
cd $TESTING_DB_DOCKER_CONTEXT
docker build -t mysql-test:init . -f $TESTING_DB_DOCKER_FILE
# create required network
docker network  create --attachable incubator-network
