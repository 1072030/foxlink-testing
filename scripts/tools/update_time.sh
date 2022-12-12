. scripts/testings/envs.sh
# shift time
SHIFT_TIME_T1="$(date --date='-5 minutes' +'%Y-%m-%d %H:%M:%S')"
SHIFT_TIME_T2="$(date --date='+5 minutes' +'%Y-%m-%d %H:%M:%S')"
python -m app.update_shift_time "$SHIFT_TIME_T1" "$SHIFT_TIME_T2"