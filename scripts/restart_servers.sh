cd $DEVELOPE_PROJECT_DIR
docker compose kill emqx
docker compose rm -f emqx
docker compose create emqx
docker compose start emqx
