import argparse
import os
import time

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--n', default=1)
args = parser.parse_args()

streams = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19,21,23,25,27,29,31]
for i in streams[:int(args.n)]:
    #print(f"python3 cve44487.py -s {i}")
    os.popen(f"python cve44487.py -s {i}")

# for j in range(100):
#     for i in streams[:int(args.n)]:
#     #     #print(f"python3 cve44487.py -s {i}")
#         os.popen(f"python cve44487.py -s {i}")
#     start_time = time.perf_counter()
#     while time.perf_counter() - start_time < 0.1:
#         pass
#     for i in streams[int(args.n):]:
#         #     #print(f"python3 cve44487.py -s {i}")
#         os.popen(f"python cve44487.py -s {i}")
#     start_time = time.perf_counter()
#     while time.perf_counter() - start_time < 1:
#         pass