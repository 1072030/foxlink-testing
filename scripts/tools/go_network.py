import sys
import subprocess
import time
from print_color import print


if __name__ == '__main__':
    t = 60
    if len(sys.argv) > 1:
        t = int(sys.argv[1])
    
    
    subprocess.run(["docker", "network", "disconnect", "incubator-network", "incubator"])
    subprocess.run(["docker", "network", "disconnect", "incubator-network", "emqx-test"])
    print("===== Network Disconnected =====", tag='log', tag_color='green', color='magenta')
    # 60s
    print_str = ['D', 'i', 's', 'c', 'o', 'n', 'n', 'e', 'c', 't', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        s = ""
        for i in range(len(print_str)):
            if i >= 11 and i <= 15:
                s += timer[i - 11]
            else:
                s += print_str[i]

        print(s, end="\r", color='red', background='grey')
        time.sleep(1)
        t -= 1
        print_str.append(print_str.pop(0))
    subprocess.run(["docker", "network", "connect", "incubator-network", "incubator"])
    subprocess.run(["docker", "network", "connect", "incubator-network", "emqx-test"])
    print("===== Network Connected =====", tag='log', tag_color='green', color='magenta')
    
