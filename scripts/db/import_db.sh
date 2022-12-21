HOST=127.0.0.1
PORT=27001
USER=root
DB_NAME=foxlink
MYSQL_PWD=AqqhQ993VNto


if [[ -z $1 ]];
then
    echo "missiong target database..."
    exit 0
fi

echo "Importing DB... $1"
mysqladmin -h $HOST -P $PORT -u $USER create -p$MYSQL_PWD $DB_NAME
mysql -h $HOST -P $PORT -u $USER $DB_NAME -p$MYSQL_PWD < $1
echo "Done !"
