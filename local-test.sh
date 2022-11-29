# after modify testing envs.sh
bash scripts/systems/create_components.sh
bash scripts/systems/clean_server.sh all
bash scripts/systems/start_server.sh emqx
bash scripts/systems/start_server.sh incubator
bash scripts/systems/start_server.sh db $1
sleep 5
bash scripts/tools/init_db.sh event


