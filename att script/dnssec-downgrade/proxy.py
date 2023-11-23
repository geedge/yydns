# -*- coding: utf-8 -*-

import socket
import dns.message
import dns.rdatatype
import dns.rdata
import dns.rdataclass
import binascii
import csv
import datetime

from scapy.all import *

#from crypto.PublicKey import Ed448
#import dns.rdatatype

# 定义代理服务器的地址和端口
proxy_host = '10.0.8.14'  # 代理服务器的IP地址
proxy_port = 53  # 代理服务器的端口
#proxy_port =  22  # 代理服务器的端口

# 定义上游DNS服务器的地址和端口
upstream_host = '127.0.0.1'  # 上游DNS服务器的IP地址
upstream_port = 9999  # 上游DNS服务器的端口

csv_file = "dnssec_log.csv"

def proxy_dns_request(request, client_addr, proxy_socket):
    # 创建与上游DNS服务器的套接字连接
    upstream_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # 发送DNS请求到上游DNS服务器
    upstream_socket.sendto(request, (upstream_host, upstream_port))

    # 接收上游DNS服务器的响应
    response, _ = upstream_socket.recvfrom(4096)

    # 修改DNS应答中的字段
    modified_response = modify_dns_response(response,client_addr,len(request))
    #modified_response = response

    # 将修改后的DNS应答发送给客户端
    #client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #client_socket.sendto(modified_response, client_addr)
    proxy_socket.sendto(modified_response, client_addr)
    # print("finish",client_addr)
    # 关闭套接字连接
    upstream_socket.close()
    #client_socket.close()

def modify_dns_response(response,client_addr,len_request):
    # 在这里添加你的修改逻辑
    # 解析DNS应答消息，并修改需要的字段
    # 可以使用dnspython等DNS库来解析和构造DNS消息
  #  print("response ",response)
    dns_response = dns.message.from_wire(response)
    # print("dns_response ",dns_response)
    qweasd = 0
    
    packet = DNS(response)
        # 解析DNS流量
    if DNS in packet:
        dns1 = packet[DNS]
        if dns1.qd[0].qtype != 1:
            print("************No Change************")
            return response
        if dns1.ancount > 0:
            print("Answers:")
            for an in dns1.an:
                print("  Name:", an.rrname.decode())
                print("  Type:", an.type)
                #print("  Data:", an.rdata)

    for rrset in dns_response.answer:
        if rrset.rdtype == dns.rdatatype.RRSIG and qweasd == 0  :
            qweasd = 1
            current_time = datetime.now()
            # with open(csv_file, "a", newline="") as file:
                # writer = csv.writer(file)
                # writer.writerow([client_addr, len_request, current_time])
            # print("dnssec_log.csv:",csv_file)
            # new_rdata = dns.rdata.from_text(rrset.rdclass, rrset.rdtype, rrset.to_text())
            # new_rdata.algorithm = 16  # 设置为 5 或其他你想要的值

            # 替换原始 RRSIG 记录
            # rrset.clear()
            # rrset.add(new_rdata)
            # for attrr in dir(rrset):
                # print(attrr)
#     print("rdata.algorithm",rrset.algorithm)
            # new_rdata = dns.rdatatype.from_text(rdtype_text.replace(dns.rdatatype.RSASHA1,dns.rdatatype.ED448))
            # rrset.items = new_rdata
       #     print(rrset.items)
 #           print(rrset[1])
#            print(bin(rrset.items[1]))
     #       for qwe in rrset:
                #print(qwe)
                #print(type(qwe)," key:   ",qwe,"   qweqweqweqweqwe           ")   
     #           for attrr in dir(qwe):
     #               print(attrr)
     #           qwe.algorithm = 16
            #    print(qwe.algorithm)
    # 遍历DNS响应中的资源记录
    
            modified_response = dns_response.to_wire()
            binary_string = bin(int(binascii.hexlify(modified_response), 16))
      #      print("len: ",len(binary_string),"\n",binary_string)
            formatted_string = str(binary_string)
            index = str(binary_string).find("01100101001000001101110000001111")
            new_string = formatted_string[:index+1] + '0' + formatted_string[index+2:]
            new_string = new_string[:index+2] + '1' + new_string[index+3:]
            new_string = new_string[:index+3] + '0' + new_string[index+4:]
            new_string = new_string[:index+4] + '0' + new_string[index+5:]
            new_string = new_string[:index+5] + '1' + new_string[index+6:]
            new_string = new_string[:index+6] + '0' + new_string[index+7:]
            formatted_string = new_string[:index+7] + '1' + new_string[index+8:]

            # index = str(binary_string).find("0000010100000011")
            index = str(binary_string).find("0000110100000011")

#    formatted_string = str(binary_string)
            new_string = formatted_string[:index+1] + '1' + formatted_string[index+2:]
            new_string = new_string[:index+2] + '1' + new_string[index+3:]
            new_string = new_string[:index+3] + '1' + new_string[index+4:]
            new_string = new_string[:index+4] + '0' + new_string[index+5:]
            new_string = new_string[:index+5] + '0' + new_string[index+6:]
            new_string = new_string[:index+6] + '0' + new_string[index+7:]
            formatted_string = new_string[:index+7] + '0' + new_string[index+8:]
   # print("len: ",len(formatted_string),"\n",formatted_string) 
   # print("index: ",formatted_string[index:])
            binary_string = formatted_string[2:]
            binary_number = int(binary_string, 2)
            formatted_string = binary_number.to_bytes((binary_number.bit_length() + 7) // 8, 'big')
     #       print("index: ",formatted_string)
            try:
                dns_response = dns.message.from_wire(formatted_string)
            except:
                modified_response = dns_response.to_wire()
     #       print(dns_response)
    modified_response = dns_response.to_wire()
    print("**********************************************************************************************************************")
    return modified_response

def start_proxy_server():
    # 创建代理服务器的套接字
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 将套接字绑定到代理服务器的地址和端口
    proxy_socket.bind((proxy_host, proxy_port))

    # 循环监听客户端请求并代理流量

    num = 1
    
    print("START:  ")
    while True:
        
        print("start")
        request, client_addr = proxy_socket.recvfrom(4096)
        print("num: ",num)
        num = num + 1
        try:
            packet = DNS(request)
            # 解析DNS流量
            if DNS in packet:
                dns1 = packet[DNS]
                if dns1.qdcount > 0:
                    print("Queries:")
                    for qd in dns1.qd:
                        print("  Query Name:", qd.qname.decode())
                        print("  Query Type:", qd.qtype)
                        print("  Query Class:", qd.qclass)
                        query_current_time = datetime.now()
                        query_current_time = query_current_time.strftime("%H%M%S%f")[:-2]
                    #    src = request[IP].src
                        print("  Query src:", client_addr)
                        print("  Query Current Time:", query_current_time)
                        tmp = qd.qname.decode()
                        if tmp[0] == "D":
                            with open("shiyan1_query", "a", newline="") as file:
                                writer = csv.writer(file)
                                writer.writerow([qd.qname.decode(), qd.qtype, qd.qclass, client_addr, query_current_time])
                            print("finish")
        except Exception as e:
            print("error",str(e))



        proxy_dns_request(request, client_addr, proxy_socket)

    # 关闭套接字连接
    proxy_socket.close()


# 启动代理服务器
start_proxy_server()
