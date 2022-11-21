cd /home/od/Desktop/repos/foxlink-api-backend/
docker compose kill emqx
docker compose rm -f emqx
docker compose create emqx
docker compose start emqx
