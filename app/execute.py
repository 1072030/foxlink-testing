import json
import signal
import argparse
import multiprocessing
import app.foxlinkevent as fevents
from datetime import datetime
from app.services.worker import worker
import time
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

    start_time = datetime.utcnow()
    processes = [
        *create_worker_behaviour_process(),
    ]

    for p in processes:
        p.start()
        time.sleep(0.1)

    event_generator = multiprocessing.Process(target=fevents.entry_point)
    event_generator.start()
    event_generator.join()
    logger.warning("FOxliNk EveNt Complete...")

    for p in processes:
        p.join()

    logger.warning("Duration: {}".format(datetime.utcnow() - start_time))
    logger.warning("============= DONE ==============")
  

def create_worker_behaviour_process():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='json')
    parser.add_argument("-n",dest="speed",type=int,default=1)
    args, unknown = parser.parse_known_args()
    
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
                    i + 1,
                    args.speed
                )
            )
            for i in range(len(worker_behaviour))
        ]


if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')
    entry_point()
    
