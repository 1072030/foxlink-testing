import sys
from datetime import datetime
from app.services.api import set_shift_time

if __name__ == "__main__":
    if (len(sys.argv) < 3):
        print(sys.argv)
        print("error!")
        exit(0)

    d1 = datetime.fromisoformat(sys.argv[1]).time()
    d2 = datetime.fromisoformat(sys.argv[2]).time()

    print(set_shift_time(0, d1, d2))
    print(set_shift_time(1, d2, d1))
