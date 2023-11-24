package main

import (
	"errors"
	"flag"
	"fmt"
	"math/rand"
	"net"
	"os"
	"strconv"

	"github.com/google/gopacket"
	"github.com/google/gopacket/layers"
	"github.com/google/gopacket/pcap"
)

// 各层的定义
var ethernetLayer *layers.Ethernet
var debugOutput = false
var handle *pcap.Handle
var repeatTime = 100

func main() {
	// 读取参数配置
	ifaceNameArg := flag.String("i", "vmnet1", "用于发送查询包的网络端口")
	sourceaddrArg := flag.String("saddr", "", "伪造报文的源地址")
	targetaddrArg := flag.String("taddr", "", "目标权威的地址")
	qnameArg := flag.String("q", "www.baidu.com.", "请求查询的域名")
	debugOutputArg := flag.Bool("d", false, "debug模式输出")
	flag.Parse()

	// 指针->值
	ifaceName := *ifaceNameArg
	sourceaddr := *sourceaddrArg
	targetaddr := *targetaddrArg
	qname := *qnameArg
	debugOutput = *debugOutputArg
	defer os.Exit(0)

	handle, _ = pcap.OpenLive(
		ifaceName,
		65536,
		true,
		pcap.BlockForever,
	)

	// 构造MAC层
	var srcmac net.HardwareAddr
	var dstmac net.HardwareAddr
	if ifaceName == "" {
		ifaceName = "eth0"
	}

	// 源MAC
	loiface, err := net.InterfaceByName(ifaceName)
	if err != nil {
		fmt.Println(err.Error())
	}
	srcmac = loiface.HardwareAddr
	if debugOutput {
		fmt.Println("源MAC地址为: " + srcmac.String())
	}

	// 目的MAC
	// 获取网关地址
	gwIP, _ := getv6Gateway()
	fmt.Println("网关IPv6地址为:" + gwIP.String())
	dstmac, err = GetGatewayIPv6Addr(loiface, gwIP)
	if err != nil {
		fmt.Println(err.Error())
	}
	if debugOutput {
		fmt.Println("目的MAC地址为: " + dstmac.String())
	}

	// mac层包
	ethernetLayer = &layers.Ethernet{
		SrcMAC:       srcmac,
		DstMAC:       dstmac,
		EthernetType: layers.EthernetTypeIPv6,
	}

	// dns查询
	for i := 0; i < repeatTime; i++ {
		go sendDNSRequest(uint16(rand.Uint32()), qname, net.ParseIP(sourceaddr), net.ParseIP(targetaddr))
	}
	if debugOutput {
		fmt.Println("已连续发送" + strconv.Itoa(repeatTime) + "个请求包到" + targetaddr)
	}
}

func Send(handle *pcap.Handle, l ...gopacket.SerializableLayer) error {
	opts := gopacket.SerializeOptions{
		FixLengths:       true,
		ComputeChecksums: true,
	}
	buffer := gopacket.NewSerializeBuffer()
	if err := gopacket.SerializeLayers(buffer, opts, l...); err != nil {
		return err
	}
	err := handle.WritePacketData(buffer.Bytes())
	if err != nil {
		println(err.Error())
	}
	return nil
}

func GetIfaceAddr(iface *net.Interface) (net.IP, error) {
	addrs, err := iface.Addrs()
	if err != nil {
		return nil, errors.New("can not get ip address")
	}

	var srcIP net.IP
	for _, address := range addrs {
		if ipnet, ok := address.(*net.IPNet); ok && !ipnet.IP.IsLoopback() {
			if ipnet.IP.To16() != nil {
				srcIP = ipnet.IP.To16()
				break
			}
		}
	}

	if srcIP == nil {
		return nil, errors.New("can not get ip address")
	}

	return srcIP, nil
}

func GetGatewayIPv6Addr(iface *net.Interface, gatewayIP net.IP) (net.HardwareAddr, error) {
	gwMAC, err := getGatewayV6Mac(iface.Name, gatewayIP)
	if err != nil {
		fmt.Println(err.Error())
		panic("")
	}
	return gwMAC, nil
}

func sendDNSRequest(id uint16, name string, resolverIP net.IP, authIP net.IP) {
	if debugOutput {
		fmt.Println("Send new DNS request", name, id, resolverIP.String(), authIP.String())
	}
	_sendDNSRequest(id, name, resolverIP, authIP, (layers.UDPPort)(rand.Uint32()), 53)
}

func _sendDNSRequest(id uint16, name string, src net.IP, dst net.IP, sport layers.UDPPort, dport layers.UDPPort) {
	ipLayer := layers.IPv6{
		FlowLabel:  1,
		SrcIP:      src,
		DstIP:      dst,
		Version:    6,
		HopLimit:   64,
		NextHeader: layers.IPProtocolUDP,
		//Flags:      layers.IPv4DontFragment,
	}
	udpLayer := layers.UDP{
		SrcPort: sport,
		DstPort: dport,
	}
	dnsLayer := layers.DNS{
		ID:           id,
		QR:           false,
		OpCode:       0,
		AA:           false,
		TC:           false,
		RD:           true,
		RA:           false,
		Z:            0,
		ResponseCode: 0,
		QDCount:      1,
		ANCount:      0,
		NSCount:      0,
		ARCount:      0,
		Questions: []layers.DNSQuestion{{
			Name:  []byte(name),
			Type:  layers.DNSTypeAAAA,
			Class: layers.DNSClassIN,
		}},
		Authorities: nil,
		Additionals: nil,
	}

	err := udpLayer.SetNetworkLayerForChecksum(&ipLayer)
	if err != nil {
		fmt.Println("udpLayer.SetNetworkLayerForChecksum @ dns.go pos 0 error", err)
	}
	err = Send(handle, ethernetLayer, &ipLayer, &udpLayer, &dnsLayer)
	if err != nil {
		fmt.Println("can not send packet @ sendDNSRequest: ", err)
	}
}
