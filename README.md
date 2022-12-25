# Installation Guide
## Steps
| **ACTION**      | **COMMAND**                                                             | **DESCRIPTION**                               |
| :-------------- | :---------------------------------------------------------------------- | :-------------------------------------------- |
| build           | conda create -n {name} python=3.8                                       | create a conda environment with python=3.8    |
| run             | bash setup.sh                                                           | to install required packages and dependencies |
| configure       | vim scripts/systems/envs.sh                                             | to configure the container settings           |
| run             | bash scripts/systems/create_components.sh                               | to build the container environment            |
| run             | bash scripts/systems/{start_server,clean_server}.sh {incubator,db,emqx} | to start container.                           |
| run`(optional)` | bash scripts/tools/init_db.sh {event,api incubator}                     | to initialize databases.                      |
| configure       | vim scripts/testing/envs.sh                                             | to configure the scenario settings.           |
| run             | bash scripts/testings/runner.sh {local,remote}                          | to start the scenario testing.                |
## Motivation
| **FOLDERS**      | **DESCRIPTION**                                                                                       |
| :--------------- | :---------------------------------------------------------------------------------------------------- |
| *scripts/systems | related to control/setup of system-wise elements such as the testing containers and network services. |
| scripts/testings | related to running the scenario testing components.                                                   |
| scripts/tools    | miscellaneous functions for scenario testing, networking and table building.                          |
| scripts/db       | related to database backup and restoration operations.                                                |




    