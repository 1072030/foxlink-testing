from datetime import datetime
from app.services.thread import WorkerThread
import  argparse
import logging
import json

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='json')
    args = parser.parse_args()
    
    worker_behaviour = None
    thread_num = 0
    with open(f'./app/scenario/{args.json}.json') as jsonfile:
        config = json.load(jsonfile)
        thread_num = len(config['worker_behavier'])
        print(f"Thread Num:{thread_num} loaded")
        worker_behaviour = config['worker_behavier']

    print(f"Scenario:{args.json} loaded")
    start_time = datetime.now()
    print(f"Start at:{start_time}")
    worker_thread = []
    print(f"Creating Threads.")
    for i in range(thread_num):
        worker_thread.append(WorkerThread(worker_behaviour[i]['username'], worker_behaviour[i]['behavier'], i))
        worker_thread[i].start()
    print(f"Running Threads.")
    for i in range(thread_num):
        worker_thread[i].join()
    print(f"Workers Complete.")
    logging.warning("============= DONE ==============")
    logging.warning(datetime.now() - start_time)
