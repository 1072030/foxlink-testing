import json
import signal
import app.worker as aw
import argparse
import multiprocessing
import app.foxlinkevent as fevents
from datetime import datetime
from app.services.thread import worker
import logging

logger = logging.getLogger("execute-server")



def cleanup_childrens(*args,**_args):
    active = multiprocessing.active_children()
    for p in active:
        p.terminate()

    logger.info(f"all sub-process terminated!!!(totally:{len(active)})")

def entry_point():
    
    signal.signal(signal.SIGINT, cleanup_childrens)
    signal.signal(signal.SIGTERM, cleanup_childrens)

    start_time = datetime.now()
    processes = [
        *create_worker_behaviour_process(),
        multiprocessing.Process(target=fevents.entry_point)
    ]
    for p in processes:
        p.start()

    for p in processes:
        p.join()

    logger.warning("Duration: {}".format(datetime.now() - start_time))
    logger.warning("============= DONE ==============")
  

def create_worker_behaviour_process():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='json')
    args = parser.parse_args()
    
    with open(f'./app/scenario/{args.json}.json') as jsonfile:

        print(f"Scenario:{args.json} loaded")

        config = json.load(jsonfile)

        worker_behaviour = config['worker_behavier']
        
        print(f"# of Workers: {len(worker_behaviour)}...")
    
        return [ 
            multiprocessing.Process(
                target=worker,
                args=(
                    worker_behaviour[i]['username'],
                    worker_behaviour[i]['behavier'],
                    i + 1
                )
            )
            for i in range(len(worker_behaviour))
        ]


if __name__ == "__main__":
    multiprocessing.set_start_method('forkserver')
    entry_point()
    