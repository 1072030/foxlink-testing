bash server_exec.sh \
"docker network $1 foxlink-api-backend_backend foxlink-api-backend_foxlink-backend_1; \
docker network $1 foxlink-api-backend_backend foxlink-api-backend_foxlink-daemon_1; \
docker network $1 foxlink-api-backend_backend foxlink-api-backend_mysql_1;"