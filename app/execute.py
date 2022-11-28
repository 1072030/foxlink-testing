import multiprocessing
import app.foxlinkevent as af
import app.worker as aw
import signal

def cleanup_childrens(*args,**_args):
    active = multiprocessing.active_children()
    for p in active:
        p.terminate()
    print(f"All Childrens Killed!!!(totally:{len(active)})")

def main():
    signal.signal(signal.SIGINT, cleanup_childrens)
    signal.signal(signal.SIGTERM, cleanup_childrens)
    processes = [
        multiprocessing.Process(target=af.main),
        multiprocessing.Process(target=aw.main)
    ]

    for p in processes:
        p.start()

    for p in processes:
        p.join()


if __name__ == "__main__":
    main()
    