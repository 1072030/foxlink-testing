docker kill mysql-test
docker rm mysql-test
echo "Container Killed!"
if [ -z $1 ]
then
    IMAGE="mysql-test:init"
else
    IMAGE=$1
fi
echo "Running Image: $IMAGE"
# echo $IMAGE
docker run -dt\
     -p 27001:3306\
     -e MYSQL_DATABASE=foxlink \
     -e MYSQL_ROOT_PASSWORD=AqqhQ993VNto \
     --name mysql-test \
     --network foxlink-api-backend_backend \
     $IMAGE
echo "Container Started!"