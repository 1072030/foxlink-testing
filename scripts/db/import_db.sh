HOST=127.0.0.1
PORT=27001
USER=root
DB_NAME=foxlink
PASSWD=AqqhQ993VNto


if [[ -z $1 ]];
then
    echo "missiong target database..."
    exit 0
fi

echo "Importing DB... $1"
mysqladmin -h $HOST -P $PORT -u $USER --password=$PASSWD -p create $DB_NAME
mysql -h $HOST -P $PORT -u $USER -p $DB_NAME --password=$PASSWD < $1
echo "Done !"
