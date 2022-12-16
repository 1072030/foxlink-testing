HOST=127.0.0.1
PORT=27001
USER=root
DB_NAME=foxlink
PASSWD=AqqhQ993VNto

echo "Importing DB..."
mysqladmin -h $HOST -P $PORT -u $USER --password=$PASSWD -p create $DB_NAME
mysql -h $HOST -P $PORT -u $USER -p $DB_NAME --password=$PASSWD < $1
echo "Done !"
