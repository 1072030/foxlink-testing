import subprocess
import time
from print_color import print

t = 60

if __name__ == '__main__':
    subprocess.run(["docker", "network", "disconnect", "incubator-network", "incubator"])
    subprocess.run(["docker", "network", "disconnect", "incubator-network", "emqx-test"])
    print("===== Network Disconnected =====", tag='log', tag_color='green', color='magenta')
    # 60s
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r", color='red', format='underline', background='grey')
        time.sleep(1)
        t -= 1

    subprocess.run(["docker", "network", "connect", "incubator-network", "incubator"])
    subprocess.run(["docker", "network", "connect", "incubator-network", "emqx-test"])
    print("===== Network Connected =====", tag='log', tag_color='green', color='magenta')
