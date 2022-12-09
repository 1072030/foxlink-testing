. scripts/testings/envs.sh

if [[ $1 == "local" ]];
then

    # reset foxlink database
    bash scripts/systems/clean_server.sh db
    bash scripts/systems/start_server.sh db $SCENARIO_DB_TAG
    # reset mqtt server
    bash scripts/systems/clean_server.sh emqx
    bash scripts/systems/start_server.sh emqx
    sleep 10
    bash scripts/systems/clean_server.sh incubator
    bash scripts/systems/start_server.sh incubator
elif [[ $1 == "reset" ]];
then
    # reset foxlink database
    bash scripts/systems/clean_server.sh db
    bash scripts/systems/start_server.sh db init
    # reset mqtt server
    bash scripts/systems/clean_server.sh emqx
    bash scripts/systems/start_server.sh emqx
    sleep 10
    bash scripts/systems/clean_server.sh incubator
    bash scripts/systems/start_server.sh incubator
    sleep 10
    bash scripts/tools/init_db.sh event
    bash scripts/tools/init_db.sh api incubator
    exit 0

elif [[ $1 == "template" ]];
then
    # reset foxlink database
    bash scripts/systems/clean_server.sh db
    bash scripts/systems/start_server.sh db template

    # reset mqtt server
    bash scripts/systems/clean_server.sh emqx
    bash scripts/systems/start_server.sh emqx

    bash scripts/systems/clean_server.sh incubator
    bash scripts/systems/start_server.sh incubator
    exit 0
else
    echo "please specify the valid condition..."
    exit 0
fi


sleep 2
echo "Running $SCENARIO...."

if [ $SCENARIO == "test5" ];
then
    # shift time
    SHIFT_TIME_T1="$(date --date='-5 minutes' +'%Y-%m-%d %H:%M:%S')"
    SHIFT_TIME_T2="$(date --date='+5 minutes' +'%Y-%m-%d %H:%M:%S')"
    python -m app.update_shift_time "$SHIFT_TIME_T1" "$SHIFT_TIME_T2"

    SHIFT_TIME_T1="$(date --date='-5 minutes' +'%Y-%m-%d %H:%M:%S')"
    SHIFT_TIME_T2="$(date --date='+5 minutes' +'%Y-%m-%d %H:%M:%S')"
    # create time
    python -m app.utils.create_time -f $SCENARIO -s "$SHIFT_TIME_T2"
elif [ $SCENARIO == "test7" ];
then
    python -m app.utils.create_time -f $SCENARIO -b 60
else
    echo "skipping the create time scenario ....."
    # create time
    python -m app.utils.create_time -f $SCENARIO 
fi


# run test case
python -m app.execute $SCENARIO -n 1
