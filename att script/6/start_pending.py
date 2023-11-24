import os
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--n', default=3)
parser.add_argument('-round', '--round', default=5)
parser.add_argument('-wait', '--wait', default=150)
args = parser.parse_args()
stime = time.perf_counter()
round = int(args.round)
wait_time = int(args.wait)
for i in range(int(args.n)):
    #print(f"python3 cve44487.py -s {i}")
    os.popen(f"python att_pending_cookie.py -stime {stime} -round {round} -wait {wait_time}")
while True:
    current_time = time.perf_counter()
    elapsed_time = current_time - stime
    print(f"经过的时间：{elapsed_time:.2f}秒", end="\r")
    time.sleep(1)  # 暂停一秒钟