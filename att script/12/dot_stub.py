import socket
import ssl
import dns.message
import dns.query
import dns.rcode
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-dot', '--dot', default='dns.alidns.com')
args = parser.parse_args()
print(f'DoT server: {args.dot}')
upstream_server = '47.88.31.213'

# 创建监听socket
listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
listener.bind(('127.0.0.1', 53))

# 创建TLS连接
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
while True:
        # 接收DNS请求
    data, addr = listener.recvfrom(1024)
    #print(dns.message.from_wire(data))
    data = dns.message.from_wire(data)
    if 'baidu' in data.question.__str__():
        # print(data)
        # print(addr)
        print('DNS请求：', data.question)
        # # 创建TLS连接并发送DNS请求到上游服务器
        resp = dns.query.tls(
            q=data,
            where=upstream_server,
            timeout=10,
            ssl_context=context)
        print('DNS响应：', resp.answer)
        # with socket.create_connection((upstream_server,853)) as sock:
        #     with context.wrap_socket(sock, server_hostname=upstream_server[0]) as tls_sock:
        #         tls_sock.sendall(data.to_wire())
        #         resp = tls_sock.recv(4096)

        # 将上游服务器的响应发送回客户端
        listener.sendto(resp.to_wire(), addr)
        break
