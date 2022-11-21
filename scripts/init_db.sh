cd /home/od/Desktop/repos/foxlink-testing/
python -m app.utils.reset 
set -a
. .env
set +a
cd /home/od/Desktop/repos/foxlink-api-backend/
alembic upgrade head
