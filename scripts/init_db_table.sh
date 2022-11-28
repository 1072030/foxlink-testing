sudo apt-get install libmysqlclient-dev
pip install mysqlclient
cd $TESTING_PROJECT_DIR
python -m app.utils.reset 
. scripts/load_env.sh
cd $DEVELOPE_PROJECT_DIR
bash tools/rebuild_db_table.sh
