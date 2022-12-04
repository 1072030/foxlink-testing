HOST=127.0.0.1
PORT=27001
USER=root
DB_NAME=testing_api
DB_BACKUP_NAME=test_api_backup.sql

echo "Importing DB..."
mysqladmin -h $HOST -P $PORT -u $USER -p create $DB_NAME
mysql -h $HOST -P $PORT -u $USER -p $DB_NAME < $DB_BACKUP_NAME
echo "Done !"