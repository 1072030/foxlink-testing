docker-compose kill foxlinkevent # 停止輸入 foxlinkevent 的 container
sleep 3
python app/utils/delete.py # 清除資料庫
sleep 3
cp app/env_template.py app/env.py
sed -i 's/test.json/testLogin_single.json/' app/env.py # 設定要執行的 Json 檔名
docker-compose kill clean && docker-compose up --build clean # 執行初始化
sleep 3
python app/utils/delete.py # 清除資料庫
sleep 3