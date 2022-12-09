set -a
# paths
BACKEND_SERVER_DOCKER_CONTEXT="/home/ntust-foxlink/foxlink-factory/foxlink-api-backend-beta-v9/"
BACKEND_SERVER_DOCKER_FILE="$(pwd)/dockerfiles/incubator/Dockerfile" 
TESTING_DB_DOCKER_CONTEXT="$(pwd)/dockerfiles/mysql-test/"
TESTING_DB_DOCKER_FILE="$(pwd)/dockerfiles/mysql-test/Dockerfile"

# networks
DOCKER_NETWORK=incubator-network

# database
DB_STARTUP_NAME=foxlink
DB_STARTUP_PWD=AqqhQ993VNto

set +a
