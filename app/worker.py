from datetime import datetime
from app.services.test_thread import WorkerThread
from app.env import THREAD_NUMBER, WORKER
import logging

if __name__ == '__main__':
    start_time = datetime.now()
    worker_thread = []

    for i in range(THREAD_NUMBER):
        worker_thread.append(WorkerThread(WORKER[i]['username'],  WORKER[i]['behavier']))
        worker_thread[i].start()
    
    for i in range(THREAD_NUMBER):
        worker_thread[i].join()

    logging.warning("============= DONE ==============")
    logging.warning(datetime.now() - start_time)