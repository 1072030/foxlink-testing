from app.services.worker_thread import WorkerThread

THREAD_NUMBER = 66

if __name__ == '__main__':
    worker_thread = []

    for i in range(THREAD_NUMBER):
        worker_thread.append(WorkerThread(user_id=i + 1))
        worker_thread[i].start()
    
    for i in range(THREAD_NUMBER):
        worker_thread[i].join()