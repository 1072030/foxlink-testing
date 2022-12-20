# Installation Guide
## Steps
    -   (optional) create a conda environment with python=3.8
    -   run: bash setup.sh, to install required packages and dependencies
    -   configure: scripts/systems/envs.sh, to configure the container settings
    -   run: bash scripts/systems/create_components.sh, to build the container environment
    -   run: bash scripts/systems/{start_server,clean_server}.sh {incubator,db,emqx} to control container.
    -   (optional) run: bash scripts/tools/init_db.sh {event,api} to initialize databases.
    -   (optional) run: bash scripts/tools/rerun_service_with_tags.sh {incubator,db,emqx} {tag} to save container to commit and restart.
    -   configure: scripts/testing/envs.sh, to configure the scenario settings.
    -   run: bash scripts/testings/runner.sh {local,remote} to start the scenario testing.
## Options

    