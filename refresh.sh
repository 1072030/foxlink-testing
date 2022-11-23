# Step0
python app/utils/delete.py # 清除資料庫
bash server_exec.sh \
"cd /home/ntust-foxlink/foxlink/foxlink-api-backend/;\
 bash ./update.sh"

docker-compose kill autoworker
docker-compose kill autocreate
docker-compose up --build -d autocreate
docker-compose up --build -d autoworker