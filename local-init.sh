# init
bash scripts/systems/create_components.sh
bash scripts/systems/clean_server.sh all
bash scripts/systems/start_server.sh all
sleep 10
bash scripts/tools/init_db.sh event 
bash scripts/tools/init_db.sh api incubator
# run python server in debuger
# insert factorymaps & devices & admin
# upload factory-worker-infos
# save image