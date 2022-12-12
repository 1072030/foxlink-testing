HOST=127.0.0.1
PORT=27001
USER=root
DB_NAME=foxlink
DB_BACKUP_NAME=test_api_backup_v3_shift5.sql
echo "Dump all DB..."

mysqldump --lock-all-tables -h $HOST -u $USER -P $PORT -p $DB_NAME > $DB_BACKUP_NAME

echo "Done !"
