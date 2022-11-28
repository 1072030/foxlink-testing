# reset database
bash scripts/restart_db.sh $SCENARIO_DB_IMAGE
# reset mqtt server
bash scripts/restart_servers.sh
# initialize login
python -m app.worker $LOGIN
# create time
python -m app.utils.create_time -f $SCENARIO
# run foxlinkevents
python -m app.foxlinkevent $SCENARIO
# run test case
python -m app.worker $SCENARIO