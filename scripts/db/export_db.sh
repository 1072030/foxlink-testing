HOST=127.0.0.1
PORT=27001
USER=root
DB_NAME=foxlink
PASSWD=AqqhQ993VNto
DB_BACKUP_NAME=./bk.sql
echo "Dump all DB..."
mysqldump --lock-all-tables -h $HOST -u $USER -P $PORT -p $DB_NAME --password=$PASSWD > $DB_BACKUP_NAME

echo "Done !"
